<script lang="ts">
	import { Upload, ChevronRight, ChevronDown } from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';
	import { fade, fly } from 'svelte/transition';

	// Scroll to features section smoothly
	const scrollToFeatures = () => {
		const featuresSection = document.getElementById('features');
		if (featuresSection) {
			featuresSection.scrollIntoView({ behavior: 'smooth' });
		}
	};
</script>

<section class=" flex w-full flex-col items-center gap-12 px-4 pt-24 md:px-6">
	<div class="flex w-full flex-col items-center gap-12 px-3 lg:flex-row">
		<div class="flex flex-col gap-6 lg:w-1/2" in:fade>
			<h1 class="text-4xl font-bold tracking-tighter sm:text-5xl lg:text-6xl">
				Protect Your Images with
				<span class="text-primary">Confidence</span>
			</h1>
			<p class="text-xl leading-relaxed text-muted-foreground">
				Upload, store, and secure your images with advanced protection features. Experience peace of
				mind with our cutting-edge security solutions.
			</p>
			<div class="flex flex-col gap-4 sm:flex-row">
				<Button size="lg" href="/register">
					<Upload class="mr-2 h-5 w-5" />
					Get Started Now
				</Button>
				<Button variant="outline" size="lg">
					Learn More
					<ChevronRight class="ml-2 h-4 w-4" />
				</Button>
			</div>
		</div>
		<div class="lg:w-1/2" in:fly={{ x: 100, duration: 1000 }}>
			<div class="relative">
				<div
					class="aspect-video rounded-lg bg-gradient-to-r from-primary/10 to-primary/5 shadow-xl"
				></div>
				<div class="bg-grid-white/10 absolute inset-0"></div>
			</div>
		</div>
	</div>

	<!-- Scroll down indicator -->
	<Button
		class="my-20 animate-bounce cursor-pointer transition-colors hover:text-primary"
		onclick={scrollToFeatures}
		variant="ghost"
	>
		<ChevronDown class="h-8 w-8" />
		<span class="sr-only">Scroll down</span>
	</Button>
</section>
