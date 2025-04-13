<script>
	import * as Carousel from '$lib/components/ui/carousel';
	import { Button } from '$lib/components/ui/button';
	import { ChevronLeft, ChevronRight } from 'lucide-svelte';
	import { onMount, onDestroy } from 'svelte';
	import { fade, fly } from 'svelte/transition';

	export let features = [];

	let api;
	let autoScrollInterval;
	let isPaused = false;
	let currentImageIndex = 0;

	const startAutoScroll = () => {
		autoScrollInterval = setInterval(() => {
			if (!isPaused && api) {
				if (api.selectedScrollSnap() === features.length - 1) {
					api.scrollTo(0);
				} else {
					api.scrollNext();
				}
			}
		}, 4000);
	};

	const handleMouseEnter = () => {
		isPaused = true;
	};

	const handleMouseLeave = () => {
		isPaused = false;
	};

	$: if (api) {
		api.on('select', () => {
			currentImageIndex = api.selectedScrollSnap();
		});
	}

	onMount(() => {
		startAutoScroll();
	});

	onDestroy(() => {
		if (autoScrollInterval) {
			clearInterval(autoScrollInterval);
		}
	});
</script>

<div class="relative hidden h-screen overflow-hidden lg:block">
	{#each features as feature, i}
		{#if currentImageIndex === i}
			<div class="absolute inset-0" in:fade={{ duration: 800 }} out:fade={{ duration: 800 }}>
				<img
					src={feature.image}
					alt={feature.title}
					class="h-full w-full object-cover brightness-[0.8]"
				/>
			</div>
		{/if}
	{/each}
	<div class="absolute inset-0 bg-gradient-to-b from-transparent via-black/40 to-black/60">
		<!-- Changed gradient direction -->
		<div class="relative h-full" on:mouseenter={handleMouseEnter} on:mouseleave={handleMouseLeave}>
			<Carousel.Root
				class="h-full w-full"
				bind:api
				opts={{
					loop: true,
					align: 'start'
				}}
			>
				<Carousel.Content class="absolute  bottom-0 h-full  ">
					{#each features as feature, index}
						<Carousel.Item class="h-full basis-full">
							<div class="flex h-full items-end justify-center pb-24">
								{#if currentImageIndex === index}
									<div class="relative mb-0 max-w-lg" in:slide={{ duration: 400, delay: 200 }}>
										<!-- Decorative border -->
										<div
											class="absolute -left-3 -top-3 h-full w-full rounded-lg border-2 border-primary/20"
										></div>

										<div class="relative space-y-4 rounded-lg p-6">
											<h2 class=" text-xl font-bold text-white sm:text-2xl">
												{feature.title}
											</h2>
											<p class="text-sm text-muted-foreground text-white sm:text-base">
												{feature.description}
											</p>
										</div>
									</div>
								{/if}
							</div>
						</Carousel.Item>
					{/each}
				</Carousel.Content>
			</Carousel.Root>

			<!-- Navigation dots -->
			<div class="absolute bottom-24 left-1/2 flex -translate-x-1/2 gap-2">
				{#each features as _, i}
					<button
						class="h-1.5 rounded-full transition-all duration-300 {currentImageIndex === i
							? 'w-8 bg-primary'
							: 'w-4 bg-primary/50 hover:bg-primary/70'}"
						on:click={() => api?.scrollTo(i)}
					/>
				{/each}
			</div>

			<!-- Navigation buttons -->
			<div class="absolute bottom-24 right-8 flex gap-2">
				<Button
					variant="outline"
					size="icon"
					class="h-8 w-8 rounded-full border-primary/20 hover:bg-primary/5 hover:text-primary"
					on:click={() => api?.scrollPrev()}
				>
					<ChevronLeft class="h-4 w-4" />
				</Button>
				<Button
					variant="outline"
					size="icon"
					class="h-8 w-8 rounded-full border-primary/20 hover:bg-primary/5 hover:text-primary"
					on:click={() => api?.scrollNext()}
				>
					<ChevronRight class="h-4 w-4" />
				</Button>
			</div>
		</div>
	</div>
</div>

<style>
	.active {
		opacity: 1;
		transform: translateY(0);
	}

	.text-outline-sm {
		text-shadow:
			-0.5px -0.5px 0 rgba(0, 0, 255, 0.5),
			0.5px -0.5px 0 rgba(0, 0, 255, 0.5),
			-0.5px 0.5px 0 rgba(0, 0, 255, 0.5),
			0.5px 0.5px 0 rgba(0, 0, 255, 0.5);
	}
</style>
