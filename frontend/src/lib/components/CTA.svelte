<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Shield, Star } from 'lucide-svelte';
</script>

<section class="w-full px-0 py-12">
	<div class="relative w-full overflow-hidden rounded-lg bg-primary/5 px-6 py-16 text-center">
		<div class="bg-grid-white/10 absolute inset-0"></div>
		<div class="relative w-full">
			<div class="mb-6 flex justify-center">
				<Shield class="h-12 w-12 text-primary" />
			</div>
			<h2 class="mb-4 text-4xl font-bold tracking-tighter">Ready to Secure Your Images?</h2>
			<p class="mx-auto mb-8 max-w-2xl text-lg text-muted-foreground">
				Join thousands of creators who trust us with their valuable content. Start protecting your
				images today.
			</p>
			<div class="flex flex-col items-center justify-center gap-4 sm:flex-row">
				<Button size="lg" class="min-w-[200px]">Get Started</Button>
			</div>
		</div>
	</div>
</section>
