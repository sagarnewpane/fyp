<script>
	import { goto } from '$app/navigation';
	import ImageGrid from '$lib/components/ImageGrid.svelte';
	import ImageUpload from '$lib/components/ImageUpload.svelte';
	import SearchFilter from '$lib/components/SearchFilter.svelte';

	export let data;

	let searchQuery = '';

	// Create a reactive filtered images array
	$: filteredImages = searchQuery
		? data.images.results.filter((image) =>
				image.image_name?.toLowerCase().includes(searchQuery.toLowerCase())
			)
		: data.images.results;

	// Create a modified pagination object for filtered results
	$: filteredPagination = {
		...data.pagination,
		count: searchQuery ? filteredImages.length : data.images.count,
		next: searchQuery ? null : data.images.next,
		previous: searchQuery ? null : data.images.previous,
		currentPage: data.pagination.currentPage
	};
</script>

<div class="container mx-auto px-4 py-8">
	<h1 class="mb-6 text-2xl font-bold">Image Gallery</h1>

	<div class="mb-6 space-y-4">
		<ImageUpload on:uploadSuccess={() => location.reload()} />
		<SearchFilter bind:searchQuery />
	</div>

	<ImageGrid images={filteredImages} pagination={filteredPagination} {searchQuery} />
</div>
