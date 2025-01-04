<script>
	import { Heart, Download } from 'lucide-svelte';
	import { goto } from '$app/navigation';

	export let images = [];
</script>

<section class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-4">
	{#if images.length === 0}
		<p class="col-span-full text-center text-gray-500">No images found</p>
	{:else}
		{#each images as image}
			<article
				class="overflow-hidden rounded-xl bg-white shadow-sm transition-transform hover:scale-[1.02]"
			>
				<!-- Remove the link for now since we don't have individual image routes -->
				<div class="relative aspect-square overflow-hidden bg-gray-100">
					<img src={image.image_url} alt={image.image_name} class="h-full w-full object-cover" />
				</div>
				<div class="p-4">
					<h3 class="font-medium text-gray-900">{image.image_name}</h3>
					<p class="mt-1 text-sm text-gray-500">Uploaded on {image.created_at}</p>
				</div>
			</article>
		{/each}
	{/if}
</section>
