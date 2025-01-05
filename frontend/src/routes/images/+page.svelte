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

	function handleFilters(event) {
		console.log('Filter event received:', event);
		console.log('Filter detail:', event.detail);

		const filters = event.detail;
		const params = new URLSearchParams();

		// Preserve search if exists
		const currentSearch = $page.url.searchParams.get('search');
		if (currentSearch) {
			params.set('search', currentSearch);
		}

		// Add file type filters
		if (filters.file_type && filters.file_type.length > 0) {
			console.log('Adding file types:', filters.file_type);
			filters.file_type.forEach((type) => {
				params.append('file_type', type);
			});
		}

		// Add size filters
		if (filters.size_min !== null) {
			console.log('Adding size_min:', filters.size_min);
			params.set('size_min', filters.size_min.toString());
		}
		if (filters.size_max !== null) {
			console.log('Adding size_max:', filters.size_max);
			params.set('size_max', filters.size_max.toString());
		}

		// Add sort parameter
		if (filters.sort) {
			console.log('Adding sort:', filters.sort);
			params.set('sort', filters.sort);
		}

		// Reset to page 1
		params.set('page', '1');

		const newUrl = `?${params.toString()}`;
		console.log('Final URL parameters:', newUrl);
		goto(newUrl);
	}

	function handlePageChange(newPage) {
		const params = new URLSearchParams($page.url.searchParams);
		params.set('page', newPage.toString());
		const newUrl = `?${params.toString()}`;
		console.log('Page - New URL:', newUrl);
		goto(newUrl);
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
			on:applyFilters={handleFilters}
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
