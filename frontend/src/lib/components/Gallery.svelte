<script lang="ts">
	import { Card } from '$lib/components/ui/card';
	import { fade } from 'svelte/transition';

	const images = [
		{ title: 'Nature Photography', category: 'Protected' },
		{ title: 'Portrait Collection', category: 'Secure' },
		{ title: 'Urban Landscapes', category: 'Encrypted' },
		{ title: 'Wildlife Series', category: 'Protected' },
		{ title: 'Wildlife Series', category: 'ds' }
	];
</script>

<section class="w-full px-4 py-12 md:px-6" id="gallery">
	<div class="mx-auto">
		<div class="mb-12 text-center">
			<h2 class="mb-4 text-3xl font-bold tracking-tighter">Your Protected Gallery</h2>
			<p class="mx-auto max-w-2xl text-lg text-muted-foreground">
				View your secured images in our state-of-the-art gallery system. Each image is protected
				with multiple layers of security.
			</p>
		</div>

		<div class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-5">
			{#each images as image, i}
				<div in:fade={{ delay: i * 200 }}>
					<Card
						class="group relative aspect-square cursor-pointer overflow-hidden bg-muted transition-colors hover:bg-muted/80"
					>
						<div
							class="absolute inset-0 flex flex-col items-center justify-center p-4 text-center opacity-0 transition-opacity group-hover:opacity-100"
						>
							<h3 class="font-semibold">{image.title}</h3>
							<p class="text-sm text-muted-foreground">{image.category}</p>
						</div>
					</Card>
				</div>
			{/each}
		</div>
	</div>
</section>
