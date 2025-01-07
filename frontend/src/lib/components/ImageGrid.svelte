<script>
	import { goto } from '$app/navigation';
	export let images = [];
</script>

<section class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
	{#if images.length === 0}
		<div
			class="col-span-full flex min-h-[300px] items-center justify-center rounded-xl border-2 border-dashed border-gray-200 bg-gray-50"
		>
			<div class="text-center">
				<p class="mb-1 text-gray-500">No images available</p>
				<p class="text-sm text-gray-400">Try adjusting your filters</p>
			</div>
		</div>
	{:else}
		{#each images as image}
			<a
				href="images/{image.id}"
				class="group block overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm transition-all duration-200 hover:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
			>
				<article class="relative">
					<div class="relative aspect-square overflow-hidden bg-gray-100">
						<img
							src={image.image_url}
							alt={image.image_name}
							class="h-full w-full object-cover transition-transform duration-300 ease-out group-hover:scale-105"
							loading="lazy"
						/>
					</div>

					<div
						class="absolute inset-0 flex items-end bg-gradient-to-t from-black/60 via-black/30 to-transparent opacity-0 transition-opacity duration-200 group-hover:opacity-100"
					>
						<div class="w-full p-4">
							<h3 class="truncate text-sm font-medium text-white">
								{image.image_name}
							</h3>
							<time datetime={image.created_at} class="mt-1 block text-xs text-white/90">
								{new Date(image.created_at).toLocaleDateString()}
							</time>
						</div>
					</div>
				</article>
			</a>
		{/each}
	{/if}
</section>
