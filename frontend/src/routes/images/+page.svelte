<script>
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import ImageGrid from '$lib/components/ImageGrid.svelte';
	import ImageUpload from '$lib/components/ImageUpload.svelte';
	import ImageFilters from '$lib/components/ImageFilters.svelte';
	import Pagination from '$lib/components/Pagination.svelte';

	export let data;

	function handleSearch(event) {
		const params = new URLSearchParams($page.url.searchParams);
		params.set('search', event.detail.search);
		params.set('page', '1');
		goto(`?${params.toString()}`);
	}

	function handleFilter(event) {
		const params = new URLSearchParams($page.url.searchParams);
		const filters = event.detail;

		const existingSearch = params.get('search');
		params.clear();
		if (existingSearch) params.set('search', existingSearch);

		if (filters.dateFrom) params.set('date_from', filters.dateFrom.toISOString());
		if (filters.dateTo) params.set('date_to', filters.dateTo.toISOString());
		if (filters.fileTypes?.length)
			filters.fileTypes.forEach((type) => params.append('file_type', type));
		if (filters.sizeMin) params.set('size_min', filters.sizeMin);
		if (filters.sizeMax) params.set('size_max', filters.sizeMax);
		if (filters.sortBy) params.set('sort', filters.sortBy);

		params.set('page', '1');
		goto(`?${params.toString()}`);
	}

	function handlePageChange(newPage) {
		const params = new URLSearchParams($page.url.searchParams);
		params.set('page', newPage.toString());
		goto(`?${params.toString()}`);
	}

	// Compute pagination values from data
	$: totalPages = data?.images ? Math.ceil(data.images.count / 10) : 1;
	$: currentPage = parseInt($page.url.searchParams.get('page') || '1');
</script>

<div class="container mx-auto px-4 py-8">
	<h1 class="mb-6 text-2xl font-bold">Image Gallery</h1>

	<div class="mb-6 space-y-4">
		<ImageUpload on:uploadSuccess={() => location.reload()} />
		<ImageFilters
			on:search={handleSearch}
			on:filter={handleFilter}
			searchQuery={$page.url.searchParams.get('search') || ''}
		/>
	</div>

	{#if data?.images?.results?.length > 0}
		<ImageGrid images={data.images.results} />

		{#if totalPages > 1}
			<div class="mt-6">
				<Pagination {totalPages} {currentPage} onPageChange={handlePageChange} />
			</div>
		{/if}
	{:else}
		<div class="py-10 text-center text-gray-500">No images found</div>
	{/if}
</div>
