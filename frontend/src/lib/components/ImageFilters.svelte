<script>
	import { createEventDispatcher } from 'svelte';
	import { Search, SlidersHorizontal, X } from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import * as Select from '$lib/components/ui/select';
	import { cn } from '$lib/utils';

	const dispatch = createEventDispatcher();

	export let searchQuery = '';
	let search = searchQuery;
	let searchTimeout;
	let filtersExpanded = true;

	// Initialize filter values
	let imageType = 'all';
	let sizeFilter = 'all';
	let sortBy = '-created_at';

	// Initialize selected states for Select components
	let selectedImageType = { value: 'all', label: 'All Types' };
	let selectedSizeFilter = { value: 'all', label: 'All Sizes' };
	let selectedSortBy = { value: '-created_at', label: 'Newest First' };

	// Define filter options
	const imageTypes = [
		{ value: 'all', label: 'All Types' },
		{ value: 'jpg', label: 'JPG' },
		{ value: 'png', label: 'PNG' },
		{ value: 'gif', label: 'GIF' }
	];

	const sizeOptions = [
		{ value: 'all', label: 'All Sizes' },
		{ value: 'small', label: 'Small (<1MB)' },
		{ value: 'medium', label: 'Medium (1-5MB)' },
		{ value: 'large', label: 'Large (>5MB)' }
	];

	const sortOptions = [
		{ value: '-created_at', label: 'Newest First' },
		{ value: 'created_at', label: 'Oldest First' },
		{ value: '-image_name', label: 'Name (Z-A)' },
		{ value: 'image_name', label: 'Name (A-Z)' },
		{ value: '-file_size', label: 'Size (Large to Small)' },
		{ value: 'file_size', label: 'Size (Small to Large)' }
	];

	// Handle search input
	function handleSearch() {
		if (searchTimeout) clearTimeout(searchTimeout);
		searchTimeout = setTimeout(() => {
			dispatch('search', { search });
		}, 1000);
	}

	// Handle select changes
	function onImageTypeSelect(selected) {
		if (selected) {
			selectedImageType = selected;
			imageType = selected.value;
			applyFilters();
		}
	}

	function onSizeFilterSelect(selected) {
		if (selected) {
			selectedSizeFilter = selected;
			sizeFilter = selected.value;
			applyFilters();
		}
	}

	function onSortBySelect(selected) {
		if (selected) {
			selectedSortBy = selected;
			sortBy = selected.value;
			applyFilters();
		}
	}

	// Get size range values based on filter selection
	function getSizeRangeValues(size) {
		const ranges = {
			small: { size_min: 0, size_max: 1 },
			medium: { size_min: 1, size_max: 5 },
			large: { size_min: 5, size_max: null },
			all: { size_min: null, size_max: null }
		};

		return ranges[size] || ranges.all;
	}

	// Apply filters
	function applyFilters() {
		const filterData = {
			file_type: imageType !== 'all' ? [imageType] : [],
			...(sizeFilter !== 'all'
				? getSizeRangeValues(sizeFilter)
				: { size_min: null, size_max: null }),
			sort: sortBy
		};

		dispatch('applyFilters', filterData);
	}

	// Reset filters
	function handleReset() {
		selectedImageType = { value: 'all', label: 'All Types' };
		selectedSizeFilter = { value: 'all', label: 'All Sizes' };
		selectedSortBy = { value: '-created_at', label: 'Newest First' };

		imageType = 'all';
		sizeFilter = 'all';
		sortBy = '-created_at';

		applyFilters();
	}

	// Toggle filters on mobile
	function toggleFilters() {
		filtersExpanded = !filtersExpanded;
	}
</script>

<div class="mb-8 w-full">
	<!-- Header Section with Toggle -->
	<div class="mb-5 flex items-center justify-between">
		<h2 class="text-sm font-semibold text-gray-500">Image Filters</h2>
		<!-- Mobile Toggle Button -->
		<Button variant="ghost" size="sm" on:click={toggleFilters} class="text-gray-500 md:hidden">
			{filtersExpanded ? 'Hide Filters' : 'Show Filters'}
			<SlidersHorizontal class="ml-2 h-4 w-4" />
		</Button>
	</div>

	<!-- Filters Container -->
	<div
		class={cn(
			'transition-all duration-300 ease-in-out',
			filtersExpanded ? 'block' : 'hidden md:block'
		)}
	>
		<div class="flex flex-col gap-4 md:flex-row md:items-end">
			<!-- Search Input - Visually Distinguished -->
			<div class="md:w-1/3 md:border-r md:pr-4">
				<Label class="mb-1.5 block text-xs font-medium text-gray-700">Search Images</Label>
				<div class="relative">
					<Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-500" />
					<Input
						bind:value={search}
						type="search"
						placeholder="Search by name..."
						class="border-primary/20 bg-primary/5 pl-10 focus:border-primary focus:ring-1 focus:ring-primary"
						on:input={handleSearch}
					/>
				</div>
			</div>

			<!-- Visual Divider for Mobile -->
			<div class="my-2 border-t md:hidden"></div>

			<!-- Filter Options Section -->
			<div class="flex flex-1 flex-col gap-4 md:flex-row">
				<div class="flex w-full flex-col items-center md:flex-row md:items-end md:gap-4">
					<!-- Filter Label for Mobile -->
					<div class="mb-2 self-start md:hidden">
						<span class="text-xs font-medium text-gray-500">Filter Options</span>
					</div>

					<!-- Image Type Select -->
					<div class="w-full md:w-auto md:flex-1">
						<Label class="mb-1.5 block text-xs font-medium text-gray-700">Image Type</Label>
						<Select.Root
							selected={selectedImageType}
							onSelectedChange={onImageTypeSelect}
							class="w-full"
						>
							<Select.Trigger class="w-full border-gray-200 bg-gray-50">
								<Select.Value placeholder="Select type" />
							</Select.Trigger>
							<Select.Content>
								<Select.Group>
									{#each imageTypes as type}
										<Select.Item value={type.value} label={type.label} />
									{/each}
								</Select.Group>
							</Select.Content>
						</Select.Root>
					</div>

					<!-- Size Filter Select -->
					<div class="w-full md:w-auto md:flex-1">
						<Label class="mb-1.5 block text-xs font-medium text-gray-700">File Size</Label>
						<Select.Root
							selected={selectedSizeFilter}
							onSelectedChange={onSizeFilterSelect}
							class="w-full"
						>
							<Select.Trigger class="w-full border-gray-200 bg-gray-50">
								<Select.Value placeholder="Select size" />
							</Select.Trigger>
							<Select.Content>
								<Select.Group>
									{#each sizeOptions as option}
										<Select.Item value={option.value} label={option.label} />
									{/each}
								</Select.Group>
							</Select.Content>
						</Select.Root>
					</div>

					<!-- Sort By Select -->
					<div class="w-full md:w-auto md:flex-1">
						<Label class="mb-1.5 block text-xs font-medium text-gray-700">Sort By</Label>
						<Select.Root selected={selectedSortBy} onSelectedChange={onSortBySelect} class="w-full">
							<Select.Trigger class="w-full border-gray-200 bg-gray-50">
								<Select.Value placeholder="Sort by" />
							</Select.Trigger>
							<Select.Content>
								<Select.Group>
									{#each sortOptions as option}
										<Select.Item value={option.value} label={option.label} />
									{/each}
								</Select.Group>
							</Select.Content>
						</Select.Root>
					</div>

					<!-- Action Buttons -->
					<div class="mt-4 flex w-full gap-2 md:mt-0 md:w-auto">
						<Button
							variant="outline"
							size="default"
							on:click={handleReset}
							class="flex-1 md:flex-initial"
						>
							Reset
						</Button>
						<Button
							on:click={applyFilters}
							class="flex-1 bg-primary hover:bg-primary/90 md:flex-initial"
						>
							Apply
						</Button>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>
