<script lang="ts">
	import { fly, fade, crossfade } from 'svelte/transition';
	import { quintOut } from 'svelte/easing';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { Button } from '$lib/components/ui/button';
	import { Shield, RefreshCw, AlertCircle } from 'lucide-svelte';
	
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
			}, 3000);

			// Show final protected state
			setTimeout(() => {
				showFinal = true;
				showCombined = false;
			}, 4500);
		}, 7000);
	}

	function stopAnimationLoop() {
		if (animationInterval) {
			clearInterval(animationInterval);
		}
	}

	onMount(() => {
		loadImage();
		return () => stopAnimationLoop();
	});
</script>

<div class="min-h-screen bg-gradient-to-br from-background to-background/95">
	{#if isLoading}
		<div class="flex flex-col items-center justify-center h-screen">
			<div class="animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-primary mb-4"></div>
			<p class="text-muted-foreground text-lg font-medium">Loading your image...</p>
		</div>
	{:else if error}
		<div class="flex flex-col items-center justify-center h-screen">
			<div class="bg-destructive/10 border-l-4 border-destructive p-4 rounded-lg shadow-sm">
				<div class="flex">
					<div class="flex-shrink-0">
						<AlertCircle class="h-5 w-5 text-destructive" />
					</div>
					<div class="ml-3">
						<p class="text-sm text-destructive">{error}</p>
					</div>
				</div>
			</div>
			<Button 
				on:click={loadImage}
				variant="outline"
				class="mt-4"
			>
				Try Again
			</Button>
		</div>
	{:else}
		<div class="flex flex-col h-screen">
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
						{#if !isPerturbed}
							<div class="flex items-center space-x-4">
								<Button 
									on:click={() => {
										stopAnimationLoop();
										showOriginal = false;
										showNoise = false;
										showPlus = false;
										showCombined = false;
										showFinal = false;
										startAnimationLoop();
									}}
									variant="outline"
									size="sm"
								>
									<RefreshCw class="mr-2 h-4 w-4" />
									Replay Animation
								</Button>
								<Button 
									on:click={applyProtection}
									disabled={isPerturbing}
									variant="default"
									size="sm"
								>
									{#if isPerturbing}
										<div class="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-white mr-2"></div>
										Applying...
									{:else}
										<Shield class="mr-2 h-4 w-4" />
										Apply Protection
									{/if}
								</Button>
							</div>
						{/if}
					</div>
				</div>
			</header>

			<!-- Main Content -->
			<main class="flex-1 px-6 py-8">
				<div class="grid grid-cols-12 gap-8 h-full">
					<!-- Animation/Image Section -->
					<div class="col-span-8 flex items-center justify-center bg-muted/30 rounded-xl p-8">
						{#if isPerturbed}
							<!-- Show protected image -->
							<div class="relative group">
								<div class="w-[600px] h-[600px] rounded-xl overflow-hidden shadow-2xl transform transition-all duration-500 group-hover:scale-105 border-4 border-primary/20">
									<img src={perturbedImage} alt="Protected Image" class="w-full h-full object-cover" />
									<div class="noise-pattern active"></div>
									<div class="shield-effect active"></div>
									<div class="protection-badge active">Protected</div>
								</div>
							</div>
						{:else}
							<!-- Show animation -->
							<div class="relative flex items-center justify-center space-x-8">
								<!-- Original Image -->
								<div class="relative group transition-all duration-500"
									class:opacity-100={showOriginal}
									class:opacity-0={!showOriginal}
									class:translate-x-0={showOriginal}
									class:translate-x-[-150%]={!showOriginal}>
									<div class="w-[400px] h-[400px] rounded-xl overflow-hidden shadow-2xl transform transition-all duration-500 group-hover:scale-105 border border-border">
										<img src={originalImage} alt="Original Image" class="w-full h-full object-cover" />
									</div>
									<div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4">
										<p class="text-white font-medium text-center">Original Image</p>
									</div>
								</div>

								<!-- Plus Sign -->
								<div class="text-5xl text-muted-foreground font-light transition-all duration-300"
									class:opacity-100={showPlus}
									class:opacity-0={!showPlus}
									class:translate-y-0={showPlus}
									class:translate-y-10={!showPlus}>
									+
								</div>

								<!-- Noise Pattern -->
								<div class="relative group transition-all duration-500"
									class:opacity-100={showNoise}
									class:opacity-0={!showNoise}
									class:translate-x-0={showNoise}
									class:translate-x-[150%]={!showNoise}>
									<div class="w-[400px] h-[400px] rounded-xl overflow-hidden shadow-2xl transform transition-all duration-500 group-hover:scale-105 border border-border">
										<div class="w-full h-full bg-gradient-to-br from-primary/10 to-primary/5 flex items-center justify-center">
											<div class="noise-pattern"></div>
										</div>
									</div>
									<div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4">
										<p class="text-white font-medium text-center">Protection Layer</p>
									</div>
								</div>

								<!-- Combined Image (Transition State) -->
								<div class="absolute transition-all duration-700 ease-[cubic-bezier(0.25,1,0.5,1)]"
									class:opacity-100={showCombined}
									class:opacity-0={!showCombined}
									class:scale-100={showCombined}
									class:scale-95={!showCombined}>
									<div class="relative group">
										<div class="w-[500px] h-[500px] rounded-xl overflow-hidden shadow-2xl transform transition-all duration-500 group-hover:scale-105 border border-border">
											<img src={originalImage} alt="Protected Image" class="w-full h-full object-cover mix-blend-overlay" />
											<div class="absolute inset-0 bg-gradient-to-br from-primary/20 to-primary/10 opacity-70"></div>
										</div>
										<div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4">
											<p class="text-white font-medium text-center">Combining Protection</p>
										</div>
									</div>
								</div>

								<!-- Final Protected Image -->
								<div class="absolute transition-all duration-1000 ease-[cubic-bezier(0.25,1,0.5,1)]"
									class:opacity-100={showFinal}
									class:opacity-0={!showFinal}
									class:scale-100={showFinal}
									class:scale-95={!showFinal}>
									<div class="relative group">
										<div class="w-[500px] h-[500px] rounded-xl overflow-hidden shadow-2xl transform transition-all duration-500 group-hover:scale-105 border-4 border-primary/20">
											<img src={originalImage} alt="Protected Image" class="w-full h-full object-cover mix-blend-overlay" />
											<div class="noise-pattern active"></div>
											<div class="shield-effect active"></div>
											<div class="protection-badge active">Protected</div>
										</div>
										<div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4">
											<p class="text-white font-medium text-center">Protected Image</p>
										</div>
									</div>
								</div>
							</div>
						{/if}
					</div>

					<!-- Info Section -->
					<div class="col-span-4 space-y-6">
						<div class="bg-card rounded-xl p-6 border border-border">
							<h3 class="text-lg font-semibold text-foreground mb-4">How It Works</h3>
							<p class="text-muted-foreground leading-relaxed">
								{#if isPerturbed}
									Your image has been protected with our advanced AI protection technology. The protection layer is invisible to human eyes but prevents AI models from properly analyzing the image content.
								{:else}
									We add an invisible protection layer to your images that prevents AI models from properly analyzing them while maintaining visual quality for human viewers. Click "Apply Protection" to secure your image.
								{/if}
							</p>
						</div>

						<div class="bg-primary/5 rounded-xl p-6 border border-primary/10">
							<h3 class="text-lg font-semibold text-primary mb-4">Protection Features</h3>
							<ul class="space-y-3">
								<li class="flex items-start space-x-3">
									<div class="flex-shrink-0 w-5 h-5 rounded-full bg-primary/10 flex items-center justify-center mt-0.5">
										<Shield class="h-3 w-3 text-primary" />
									</div>
									<p class="text-sm text-muted-foreground">Invisible to human eyes</p>
								</li>
								<li class="flex items-start space-x-3">
									<div class="flex-shrink-0 w-5 h-5 rounded-full bg-primary/10 flex items-center justify-center mt-0.5">
										<Shield class="h-3 w-3 text-primary" />
									</div>
									<p class="text-sm text-muted-foreground">Prevents AI model analysis</p>
								</li>
								<li class="flex items-start space-x-3">
									<div class="flex-shrink-0 w-5 h-5 rounded-full bg-primary/10 flex items-center justify-center mt-0.5">
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
		background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noiseFilter'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%' height='100%' filter='url(%23noiseFilter)' opacity='0.20'/%3E%3C/svg%3E");
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
		0% { transform: scale(0.95); opacity: 0.7; }
		50% { transform: scale(1.05); opacity: 0.9; }
		100% { transform: scale(0.95); opacity: 0.7; }
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
  