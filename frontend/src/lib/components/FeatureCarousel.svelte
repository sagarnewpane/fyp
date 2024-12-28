<script>
	import * as Carousel from '$lib/components/ui/carousel';
	import { Button } from '$lib/components/ui/button';
	import { ChevronLeft, ChevronRight } from 'lucide-svelte';
	import { onMount, onDestroy } from 'svelte';
	import { fade } from 'svelte/transition';

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
					class="h-full w-full object-cover dark:brightness-[0.2] dark:grayscale"
				/>
			</div>
		{/if}
	{/each}
	<div class="absolute inset-0 bg-black/50">
		<div class="relative h-full" on:mouseenter={handleMouseEnter} on:mouseleave={handleMouseLeave}>
			<Carousel.Root
				class="h-full w-full"
				bind:api
				opts={{
					loop: true,
					align: 'start'
				}}
			>
				<Carousel.Content class="h-full">
					{#each features as feature}
						<Carousel.Item class="h-full basis-full">
							<div class="flex h-full items-center justify-center p-8">
								<div class="max-w-xl space-y-4 text-center text-white">
									<h2 class="text-3xl font-bold">{feature.title}</h2>
									<p class="text-lg text-gray-200">{feature.description}</p>
								</div>
							</div>
						</Carousel.Item>
					{/each}
				</Carousel.Content>
			</Carousel.Root>

			<Button
				variant="ghost"
				class="absolute left-4 top-1/2 h-12 w-12 -translate-y-1/2 rounded-full bg-white/10 p-3 hover:bg-white/20 hover:text-white"
				on:click={() => api?.scrollPrev()}
			>
				<ChevronLeft class="h-6 w-6" />
			</Button>
			<Button
				variant="ghost"
				class="absolute right-4 top-1/2 h-12 w-12 -translate-y-1/2 rounded-full bg-white/10 p-3 hover:bg-white/20 hover:text-white"
				on:click={() => api?.scrollNext()}
			>
				<ChevronRight class="h-6 w-6" />
			</Button>

			<div class="absolute bottom-6 left-1/2 flex -translate-x-1/2 gap-2">
				{#each features as _, i}
					<button
						class="h-2 w-2 rounded-full transition-all {currentImageIndex === i
							? 'bg-white'
							: 'bg-white/50'}"
						on:click={() => api?.scrollTo(i)}
					/>
				{/each}
			</div>
		</div>
	</div>
</div>
