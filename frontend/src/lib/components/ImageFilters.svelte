<script>
	import { createEventDispatcher } from 'svelte';
	import { Search, SlidersHorizontal } from 'lucide-svelte';
	import { slide } from 'svelte/transition';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import * as Select from '$lib/components/ui/select';
	import { cn } from '$lib/utils';

	const dispatch = createEventDispatcher();

	export let searchQuery = '';
	let search = searchQuery;
	let searchTimeout;
	let showAdvanced = false;

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
			console.log('Image type selected:', imageType);
		}
	}

	function onSizeFilterSelect(selected) {
		if (selected) {
			selectedSizeFilter = selected;
			sizeFilter = selected.value;
			console.log('Size filter selected:', sizeFilter);
		}
	}

	function onSortBySelect(selected) {
		if (selected) {
			selectedSortBy = selected;
			sortBy = selected.value;
			console.log('Sort by selected:', sortBy);
		}
	}

	// Get size range values based on filter selection
	function getSizeRangeValues(size) {
		console.log('Getting size range for:', size);

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
		console.log('Current selections:', { imageType, sizeFilter, sortBy });

		const filterData = {
			file_type: imageType !== 'all' ? [imageType] : [],
			...(sizeFilter !== 'all'
				? getSizeRangeValues(sizeFilter)
				: { size_min: null, size_max: null }),
			sort: sortBy
		};

		console.log('Filter data being dispatched:', filterData);
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
</script>

<div class="mb-8 w-full">
	<div class="rounded-xl border bg-white p-6 shadow-sm">
		<!-- Header Section -->
		<div class="mb-6 flex items-center justify-between">
			<h2 class="text-sm font-semibold text-gray-500">Search Image</h2>
			<div class="flex items-center gap-2">
				<span class="text-sm text-gray-500">Filter & Sort</span>
			</div>
		</div>

		<!-- Search and Advanced Toggle -->
		<div class="flex gap-3">
			<div class="relative flex-1">
				<Search class="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-gray-400" />
				<Input
					bind:value={search}
					type="search"
					placeholder="Search images..."
					class="border-gray-200 bg-gray-50 pl-10"
					on:input={handleSearch}
				/>
			</div>
			<Button
				variant="outline"
				size="default"
				on:click={() => (showAdvanced = !showAdvanced)}
				class={cn(
					'inline-flex items-center gap-2',
					showAdvanced && 'border-primary/20 bg-primary/10'
				)}
			>
				<SlidersHorizontal class="h-4 w-4" />
				<span>Filters</span>
			</Button>
		</div>

		{#if showAdvanced}
			<div transition:slide class="mt-4 space-y-6">
				<div class="grid gap-4 md:grid-cols-3">
					<!-- Image Type Select -->
					<div class="space-y-2">
						<Label class="text-sm font-medium text-gray-700">Image Type</Label>
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
					<div class="space-y-2">
						<Label class="text-sm font-medium text-gray-700">File Size</Label>
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
					<div class="space-y-2">
						<Label class="text-sm font-medium text-gray-700">Sort By</Label>
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
				</div>

				<!-- Action Buttons -->
				<div class="flex justify-end gap-2 border-t pt-2">
					<Button variant="outline" on:click={handleReset} class="text-gray-600">Reset</Button>
					<Button on:click={applyFilters} class="bg-primary hover:bg-primary/90">
						Apply Filters
					</Button>
				</div>
			</div>
		{/if}
	</div>
</div>
