<script>
	import Hero from '$lib/components/Hero.svelte';
	import Features from '$lib/components/Features.svelte';
	import Gallery from '$lib/components/Gallery.svelte';
	import FAQ from '$lib/components/FAQ.svelte';
	import CTA from '$lib/components/CTA.svelte';
</script>

<main class="min-h-screen w-full bg-background text-foreground">
	<!-- Main sections with reduced gap -->
	<div class="flex flex-col gap-16">
		<Hero />
		<Features />
		<Gallery />
		<FAQ />
		<CTA />
	</div>
</main>
