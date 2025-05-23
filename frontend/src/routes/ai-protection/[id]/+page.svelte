<script lang="ts">
	import { fly, fade, crossfade } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { Button } from '$lib/components/ui/button';
	import { Shield, RefreshCw, AlertCircle, Trash2 } from 'lucide-svelte';
	import { toast } from 'svelte-sonner';
	import { Slider } from '$lib/components/ui/slider';

	let showOriginal = false;
	let showNoise = false;
	let showPlus = false;
	let showCombined = false;
	let showFinal = false;
	let originalImage = '';
	let perturbedImage = '';
	let isLoading = true;
	let isPerturbing = false;
	let isPerturbed = false;
	let error: string | null = null;
	let animationPhase = 0;
	let animationInterval: NodeJS.Timeout;
	let isRemoving = false;
	let sliderValue = [50]; // Changed to array for Slider component

	const [send, receive] = crossfade({
		duration: 800,
		easing: quintOut
	});

	// Fetch the original image and check perturbation status
	async function loadImage() {
		try {
			const response = await fetch(`/api/images/${$page.params.id}`);
			if (!response.ok) {
				throw new Error('Failed to load image');
			}
			const data = await response.json();
			console.log(data);
			originalImage = data.image_url;

			// Check AI protection status
			const protectionResponse = await fetch(`/api/images/${$page.params.id}/ai-protection/`);
			if (protectionResponse.ok) {
				const protectionData = await protectionResponse.json();
				isPerturbed = protectionData.enabled;
				perturbedImage = protectionData.protected_image;
				console.log(protectionData);
			}

			isLoading = false;

			if (!isPerturbed) {
				startAnimationLoop();
			}
		} catch (err: unknown) {
			error = err instanceof Error ? err.message : 'An unknown error occurred';
			isLoading = false;
			toast.error('Failed to load image');
		}
	}

	async function applyProtection() {
		if (isPerturbing || isPerturbed) return;

		isPerturbing = true;
		error = null;
		try {
			const response = await fetch(`/api/images/${$page.params.id}/ai-protection/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				}
			});

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.error || 'Failed to apply protection');
			}

			const data = await response.json();
			perturbedImage = data.protected_image;
			isPerturbed = true;
			stopAnimationLoop();

			// Show success notification or feedback here if needed
		} catch (err: unknown) {
			error = err instanceof Error ? err.message : 'An unknown error occurred';
			isPerturbed = false;
		} finally {
			isPerturbing = false;
		}
	}

	async function removeProtection() {
		if (isRemoving) return;

		isRemoving = true;
		error = null;
		try {
			const response = await fetch(`/api/images/${$page.params.id}/ai-protection/`, {
				method: 'DELETE'
			});

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.error || 'Failed to remove protection');
			}

			isPerturbed = false;
			perturbedImage = '';
			startAnimationLoop();

			// Show success notification
			toast.success('AI protection removed successfully');
		} catch (err: unknown) {
			error = err instanceof Error ? err.message : 'An unknown error occurred';
			toast.error('Failed to remove AI protection');
		} finally {
			isRemoving = false;
		}
	}

	function startAnimationLoop() {
		// Initial animation sequence
		setTimeout(() => {
			showOriginal = true;
		}, 100);

		setTimeout(() => {
			showNoise = true;
		}, 1000);

		setTimeout(() => {
			showPlus = true;
		}, 1500);

		setTimeout(() => {
			showCombined = true;
			showOriginal = false;
			showNoise = false;
			showPlus = false;
		}, 3000);

		setTimeout(() => {
			showFinal = true;
			showCombined = false;
		}, 4500);

		// Set up looping animation
		animationInterval = setInterval(() => {
			// Reset all states
			showOriginal = false;
			showNoise = false;
			showPlus = false;
			showCombined = false;
			showFinal = false;

			// Show original image
			setTimeout(() => {
				showOriginal = true;
			}, 100);

			// Show noise pattern
			setTimeout(() => {
				showNoise = true;
			}, 1000);

			// Show plus sign
			setTimeout(() => {
				showPlus = true;
			}, 1500);

			// Show combined state
			setTimeout(() => {
				showCombined = true;
				showOriginal = false;
				showNoise = false;
				showPlus = false;
			}, 5000);

			// Show final protected state
			setTimeout(() => {
				showFinal = true;
				showCombined = false;
			}, 5500);
		}, 10000);
	}

	function stopAnimationLoop() {
		if (animationInterval) {
			clearInterval(animationInterval);
		}
	}

	onMount(() => {
		loadImage();
		return () => {
			if (animationInterval) {
				clearInterval(animationInterval);
			}
		};
	});
</script>

<div class="min-h-screen bg-gradient-to-br from-background to-background/95">
	{#if isLoading}
		<div class="flex h-screen flex-col items-center justify-center">
			<div
				class="mb-4 h-16 w-16 animate-spin rounded-full border-b-2 border-t-2 border-primary"
			></div>
			<p class="text-lg font-medium text-muted-foreground">Loading your image...</p>
		</div>
	{:else if error}
		<div class="flex h-screen flex-col items-center justify-center">
			<div class="rounded-lg border-l-4 border-destructive bg-destructive/10 p-4 shadow-sm">
				<div class="flex">
					<div class="flex-shrink-0">
						<AlertCircle class="h-5 w-5 text-destructive" />
					</div>
					<div class="ml-3">
						<p class="text-sm text-destructive">{error}</p>
					</div>
				</div>
			</div>
			<Button on:click={loadImage} variant="outline" class="mt-4">Try Again</Button>
		</div>
	{:else}
		<div class="flex h-screen flex-col">
			<!-- Header Section -->
			<header class="border-b border-border bg-card/50 backdrop-blur-sm">
				<div class="px-6 py-4">
					<div class="flex items-center justify-between">
						<div class="flex items-center space-x-4">
							<div>
								<h1 class="text-2xl font-bold text-foreground">AI Image Protection</h1>
								<p class="text-sm text-muted-foreground">
									{#if isPerturbed}
										Your image is now protected from AI scraping
									{:else}
										See how we protect your images from AI scraping
									{/if}
								</p>
							</div>
						</div>
						<div class="flex items-center space-x-4">
							{#if isPerturbed}
								<Button
									on:click={removeProtection}
									disabled={isRemoving}
									variant="destructive"
									size="sm"
								>
									{#if isRemoving}
										<div
											class="mr-2 h-4 w-4 animate-spin rounded-full border-b-2 border-t-2 border-white"
										></div>
										Removing...
									{:else}
										<Trash2 class="mr-2 h-4 w-4" />
										Remove Protection
									{/if}
								</Button>
							{:else}
								<Button
									on:click={applyProtection}
									disabled={isPerturbing}
									variant="default"
									size="sm"
								>
									{#if isPerturbing}
										<div
											class="mr-2 h-4 w-4 animate-spin rounded-full border-b-2 border-t-2 border-white"
										></div>
										Applying...
									{:else}
										<Shield class="mr-2 h-4 w-4" />
										Apply Protection
									{/if}
								</Button>
							{/if}
						</div>
					</div>
				</div>
			</header>

			<!-- Main Content -->
			<main class="flex-1 px-6 py-8">
				<div class="grid h-full grid-cols-12 gap-8">
					<!-- Animation/Image Section -->
					<div class="col-span-8 flex items-center justify-center rounded-xl bg-muted/30 p-8">
						{#if isPerturbed}
							<!-- Show protected image with slider -->
							<div class="relative w-full max-w-[600px]">
								<div
									class="relative aspect-square w-full overflow-hidden rounded-xl border-4 border-primary/20 shadow-2xl"
								>
									<!-- Original Image -->
									<img
										src={originalImage}
										alt="Original Image"
										class="absolute inset-0 h-full w-full object-cover"
										style="clip-path: inset(0 {100 - sliderValue[0]}% 0 0);"
									/>
									<!-- Protected Image -->
									<img
										src={perturbedImage}
										alt="Protected Image"
										class="absolute inset-0 h-full w-full object-cover"
										style="clip-path: inset(0 0 0 {sliderValue[0]}%);"
									/>
									<!-- Slider Line -->
									<div
										class="absolute bottom-0 top-0 w-0.5 bg-white/50"
										style="left: {sliderValue[0]}%; transform: translateX(-50%);"
									/>
								</div>
								<!-- Slider Control -->
								<div class="mt-4 px-4">
									<Slider bind:value={sliderValue} min={0} max={100} step={1} class="w-full" />
									<div class="mt-2 flex justify-between text-sm text-muted-foreground">
										<span>Original</span>
										<span>Protected</span>
									</div>
								</div>
							</div>
						{:else}
							<!-- Show animation -->
							<div class="relative flex items-center justify-center space-x-8">
								<!-- Original Image -->
								<div
									class="group relative transition-all duration-500"
									class:opacity-100={showOriginal}
									class:opacity-0={!showOriginal}
									class:translate-x-0={showOriginal}
									class:translate-x-[-150%]={!showOriginal}
								>
									<div
										class="h-[400px] w-[400px] transform overflow-hidden rounded-xl border border-border shadow-2xl transition-all duration-500 group-hover:scale-105"
									>
										<img
											src={originalImage}
											alt="Original Image"
											class="h-full w-full object-cover"
										/>
									</div>
									<div
										class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4"
									>
										<p class="text-center font-medium text-white">Original Image</p>
									</div>
								</div>

								<!-- Plus Sign -->
								<div
									class="text-5xl font-light text-muted-foreground transition-all duration-300"
									class:opacity-100={showPlus}
									class:opacity-0={!showPlus}
									class:translate-y-0={showPlus}
									class:translate-y-10={!showPlus}
								>
									+
								</div>

								<!-- Noise Pattern -->
								<div
									class="group relative transition-all duration-500"
									class:opacity-100={showNoise}
									class:opacity-0={!showNoise}
									class:translate-x-0={showNoise}
									class:translate-x-[150%]={!showNoise}
								>
									<div
										class="h-[400px] w-[400px] transform overflow-hidden rounded-xl border border-border shadow-2xl transition-all duration-500 group-hover:scale-105"
									>
										<div
											class="flex h-full w-full items-center justify-center bg-gradient-to-br from-primary/10 to-primary/5"
										>
											<img
												src="/uap.png"
												alt="Noise Pattern"
												class="h-full w-full object-cover opacity-70"
											/>
										</div>
									</div>
									<div
										class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4"
									>
										<p class="text-center font-medium text-white">Protection Layer</p>
									</div>
								</div>

								<!-- Combined Image (Transition State) -->
								<!-- <div
									class="absolute transition-all duration-700 ease-[cubic-bezier(0.25,1,0.5,1)]"
									class:opacity-100={showCombined}
									class:opacity-0={!showCombined}
									class:scale-100={showCombined}
									class:scale-95={!showCombined}
								>
									<div class="group relative">
										<div
											class="h-[500px] w-[500px] transform overflow-hidden rounded-xl border border-border shadow-2xl transition-all duration-500 group-hover:scale-105"
										>
											<img
												src={originalImage}
												alt="Protected Image"
												class="h-full w-full object-cover mix-blend-overlay"
											/>
											<div
												class="absolute inset-0 bg-gradient-to-br from-primary/20 to-primary/10 opacity-70"
											></div>
										</div>
										<div
											class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4"
										>
											<p class="text-center font-medium text-white">Combining Protection</p>
										</div>
									</div>
								</div> -->

								<!-- Final Protected Image -->
								<div
									class="absolute transition-all duration-1000 ease-[cubic-bezier(0.25,1,0.5,1)]"
									class:opacity-100={showFinal}
									class:opacity-0={!showFinal}
									class:scale-100={showFinal}
									class:scale-95={!showFinal}
								>
									<div class="group relative">
										<div
											class="h-[500px] w-[500px] transform overflow-hidden rounded-xl border-4 border-primary/20 shadow-2xl transition-all duration-500 group-hover:scale-105"
										>
											<img
												src={originalImage}
												alt="Protected Image"
												class="h-full w-full object-cover mix-blend-overlay"
											/>
											<div class="noise-pattern active"></div>
											<div class="shield-effect active"></div>
										</div>
										<div
											class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4"
										>
											<p class="text-center font-medium text-white">Protected Image</p>
										</div>
									</div>
								</div>
							</div>
						{/if}
					</div>

					<!-- Info Section -->
					<div class="col-span-4 space-y-6">
						<div class="rounded-xl border border-border bg-card p-6">
							<h3 class="mb-4 text-lg font-semibold text-foreground">How It Works</h3>
							<p class="leading-relaxed text-muted-foreground">
								{#if isPerturbed}
									Your image has been protected with our advanced AI protection technology. A
									protection layer is applied on the image that is invisible to human eyes but
									prevents AI models from properly analyzing the image content i.e. prevent them
									from understanding your images that might be used for their training or copying
									your content.
								{:else}
									We add an invisible protection layer to your images that prevents AI models from
									properly analyzing them while maintaining visual quality for human viewers. Your
									image might be in risk of theft by AI. Click "Apply Protection" to secure your
									image.
								{/if}
							</p>
						</div>

						<div class="rounded-xl border border-primary/10 bg-primary/5 p-6">
							<h3 class="mb-4 text-lg font-semibold text-primary">Why use it?</h3>
							<ul class="space-y-3">
								<li class="flex items-start space-x-3">
									<div
										class="mt-0.5 flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-full bg-primary/10"
									>
										<Shield class="h-3 w-3 text-primary" />
									</div>
									<p class="text-sm text-muted-foreground">Invisible to human eyes</p>
								</li>
								<li class="flex items-start space-x-3">
									<div
										class="mt-0.5 flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-full bg-primary/10"
									>
										<Shield class="h-3 w-3 text-primary" />
									</div>
									<p class="text-sm text-muted-foreground">Prevents AI model analysis</p>
								</li>
								<li class="flex items-start space-x-3">
									<div
										class="mt-0.5 flex h-5 w-5 flex-shrink-0 items-center justify-center rounded-full bg-primary/10"
									>
										<Shield class="h-3 w-3 text-primary" />
									</div>
									<p class="text-sm text-muted-foreground">Maintains image quality</p>
								</li>
							</ul>
						</div>
					</div>
				</div>
			</main>
		</div>
	{/if}
</div>

<style>
	.noise-pattern {
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background-image: url('/noise-pattern.png');
		background-size: cover;
		opacity: 0;
		transition: opacity 0.5s ease-in-out;
	}

	.noise-pattern.active {
		opacity: 0.7;
	}

	.shield-effect {
		position: absolute;
		width: 100%;
		height: 100%;
		background: radial-gradient(circle at center, hsl(var(--primary) / 0.3) 0%, transparent 70%);
		opacity: 0;
		transition: opacity 0.5s ease-in-out;
	}

	.shield-effect.active {
		opacity: 1;
		animation: pulseShield 2s infinite;
	}

	@keyframes pulseShield {
		0% {
			transform: scale(0.95);
			opacity: 0.7;
		}
		50% {
			transform: scale(1.05);
			opacity: 0.9;
		}
		100% {
			transform: scale(0.95);
			opacity: 0.7;
		}
	}

	.protection-badge {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		background-color: hsl(var(--primary));
		color: hsl(var(--primary-foreground));
		padding: 0.5rem 1rem;
		border-radius: 9999px;
		font-weight: bold;
		box-shadow: 0 4px 6px -1px hsl(var(--primary) / 0.2);
		opacity: 0;
		transition: opacity 0.5s ease-in-out;
	}

	.protection-badge.active {
		opacity: 1;
	}

	/* Smooth transitions for all elements */
	* {
		transition-property: opacity, transform, filter, brightness;
		transition-timing-function: cubic-bezier(0.25, 1, 0.5, 1);
	}
</style>
