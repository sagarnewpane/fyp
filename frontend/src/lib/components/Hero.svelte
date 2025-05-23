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

<section class="flex w-full flex-col items-center gap-12 px-4 pt-24 md:px-6">
	<div class="flex w-full flex-col items-center gap-12 px-3 lg:flex-row">
		<div class="flex flex-col gap-6 lg:w-1/2" in:fade>
			<h1 class="text-4xl font-bold tracking-tighter sm:text-5xl lg:text-6xl">
				Protect Your Images with
				<span class="bg-gradient-to-r from-primary to-primary/80 bg-clip-text text-transparent">
					Confidence
				</span>
			</h1>
			<div class="decorative-circle"></div>
			<p class="text-xl leading-relaxed text-muted-foreground">
				Upload, store, and securely share your images with the world. Experience peace of mind with
				our cutting-edge protection solutions to protect your images from theft.
			</p>
			<div class="flex flex-col gap-4 sm:flex-row">
				<!-- Modified Get Started Button -->
				<Button
					href="/register"
					class="bg-[#2B6CB0] px-4 py-2 text-white transition-transform duration-300 hover:scale-105 hover:bg-[#235A94] hover:shadow-lg hover:shadow-[#2B6CB0]/20"
				>
					<Upload class="mr-2 h-5 w-5" />
					Get Started Now
				</Button>

				<!-- Modified Learn More Button -->
				<Button
					variant="ghost"
					class="relative overflow-hidden px-3 text-[#1A202C] transition-colors after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 after:bg-[#2B6CB0] after:transition-all after:duration-300 hover:text-[#2B6CB0] hover:after:w-full"
				>
					Learn More
					<ChevronRight class="ml-2 h-4 w-4" />
				</Button>
			</div>
		</div>
		<div class="lg:w-1/2" in:fly={{ x: 100, duration: 1000 }}>
			<div class="relative">
				<div
					class="aspect-video rounded-2xl bg-gradient-to-r from-primary/10 to-primary/5 shadow-lg transition-all duration-300 hover:shadow-xl"
				>
					<img
						src="/hero.png"
						alt=""
						class="absolute inset-0 h-full w-full rounded-2xl object-cover"
					/>
					<div class="absolute inset-0 rounded-2xl border border-primary/10" />
				</div>
				<div class="bg-grid-white/10 absolute inset-0 rounded-2xl" />
			</div>
		</div>
	</div>

	<Button
		class="my-20 animate-bounce cursor-pointer transition-colors hover:text-primary"
		onclick={scrollToFeatures}
		variant="ghost"
	>
		<ChevronDown class="h-8 w-8" />
		<span class="sr-only">Scroll down</span>
	</Button>
</section>

<style>
	section {
		position: relative;
	}

	section::after {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		width: 100%;
		height: 100%;
		background: radial-gradient(circle at center, var(--primary-50) 0%, transparent 70%);
		opacity: 0.1;
		pointer-events: none;
	}
</style>
