<script>
	import { Heart, Download } from 'lucide-svelte';
	import { goto } from '$app/navigation';

	export let images = [];
	export let pagination;
	export let searchQuery = ''; // Add this line to accept searchQuery as a prop

	function changePage(pageUrl) {
		if (pageUrl) {
			try {
				const url = new URL(pageUrl);
				const page = url.searchParams.get('page') || '1';
				goto(`?page=${page}`, { replaceState: false });
			} catch (err) {
				console.error('Error changing page:', err);
			}
		}
	}

	$: totalPages = Math.ceil(pagination.count / 10);
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

{#if !searchQuery && (pagination.next || pagination.previous)}
	<div class="mt-6 flex justify-center gap-4">
		{#if pagination.previous}
			<button
				class="rounded-lg bg-gray-100 px-4 py-2 hover:bg-gray-200"
				on:click={() => changePage(pagination.previous)}
			>
				Previous
			</button>
		{/if}

		<span class="px-4 py-2">
			Page {pagination.currentPage} of {totalPages || 1}
		</span>

		{#if pagination.next}
			<button
				class="rounded-lg bg-gray-100 px-4 py-2 hover:bg-gray-200"
				on:click={() => changePage(pagination.next)}
			>
				Next
			</button>
		{/if}
	</div>
{/if}
