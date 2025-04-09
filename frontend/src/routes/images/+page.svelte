<script>
	import { goto } from '$app/navigation';
	import { page } from '$app/stores';
	import { invalidate } from '$app/navigation';
	import ImageGrid from '$lib/components/ImageGrid.svelte';
	import ImageUpload from '$lib/components/ImageUpload.svelte';
	import ImageFilters from '$lib/components/ImageFilters.svelte';
	import Pagination from '$lib/components/Pagination.svelte';
	import { Button } from '$lib/components/ui/button';

	export let data;
	let showUpload = false;

	// Toggle upload section visibility
	function toggleUpload() {
		showUpload = !showUpload;
	}

	async function handleUploadSuccess() {
		// Hide the upload component
		showUpload = false;

		// Force re-fetch of the images data
		await invalidate('data:images'); // This should match your load function dependency key
	}

	function handleSearch(event) {
		const params = new URLSearchParams($page.url.searchParams);
		params.set('search', event.detail.search);
		params.set('page', '1');
		goto(`?${params.toString()}`);
	}

	function handleImageDeleted(event) {
		// Update the local data by removing the deleted image
		const deletedImageId = event.detail.imageId;
		data.images.results = data.images.results.filter((img) => img.id !== deletedImageId);
		data.images.count -= 1;
		data.images.total -= 1;
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

<main class="min-h-screen w-full bg-gray-50/50">
	<div class="w-full space-y-6 px-4 py-6 md:px-6 lg:px-8">
		<!-- Header Section -->
		<div class="flex items-center justify-between">
			<div>
				<h1 class="text-2xl font-bold tracking-tight text-gray-900">Image Gallery</h1>
				<p class="mt-1 text-sm text-gray-500">Upload, organize, and browse your images</p>
			</div>
			<!-- Upload button -->
			<Button on:click={toggleUpload}>
				{showUpload ? 'Hide Upload' : 'Upload Image'}
			</Button>
		</div>

		<!-- Upload Section - Only show if showUpload is true -->
		{#if showUpload}
			<section class="overflow-hidden rounded-lg border bg-white shadow-sm">
				<div class="border-b bg-gray-50/50 px-4 py-3 sm:px-6">
					<h2 class="font-semibold text-gray-900">Upload Images</h2>
				</div>
				<div class="p-4 sm:p-6">
					<ImageUpload on:uploadSuccess={handleUploadSuccess} />
				</div>
			</section>
		{/if}
		<!-- Upload Section -->
		<!-- <section class="overflow-hidden rounded-lg border bg-white shadow-sm">
			<div class="border-b bg-gray-50/50 px-4 py-3 sm:px-6">
				<h2 class="font-semibold text-gray-900">Upload Images</h2>
			</div>
			<div class="p-4 sm:p-6">
				<ImageUpload on:uploadSuccess={() => location.reload()} />
			</div>
		</section> -->

		<!-- Browse Images Section -->
		<section class="space-y-4">
			<div class="flex items-center justify-between px-1">
				{#if data?.images?.results?.length > 0}
					<p class="text-sm text-gray-500">
						Showing {data.images.results.length} of {data.images.total} images
					</p>
				{/if}
			</div>

			<!-- Filters and Grid Container -->
			<div class="rounded-lg border bg-white shadow-sm">
				<div class="border-b p-4 sm:p-6">
					<ImageFilters
						on:search={handleSearch}
						on:applyFilters={handleFilters}
						searchQuery={$page.url.searchParams.get('search') || ''}
					/>
				</div>

				<div class="p-4 sm:p-6">
					{#if data?.images?.results?.length > 0}
						<ImageGrid images={data.images.results} on:imageDeleted={handleImageDeleted} />

						{#if totalPages > 1}
							<div class="mt-6 border-t pt-6">
								<Pagination {totalPages} {currentPage} onPageChange={handlePageChange} />
							</div>
						{/if}
					{:else}
						<div
							class="flex min-h-[250px] flex-col items-center justify-center rounded-lg border-2 border-dashed border-gray-200 bg-gray-50/50"
						>
							<p class="text-gray-600">No images found</p>
							<p class="mt-1 text-sm text-gray-500">Try adjusting your search or filters</p>
						</div>
					{/if}
				</div>
			</div>
		</section>
	</div>
</main>
