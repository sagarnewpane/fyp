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
		}, 500);
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

<div
	class="flex w-full flex-col gap-4 rounded-lg border bg-card p-4 text-card-foreground shadow-sm"
>
	<!-- Search input -->
	<div class="flex gap-2">
		<div class="relative flex-1">
			<Search class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
			<Input
				bind:value={search}
				type="search"
				placeholder="Search..."
				class="pl-9"
				on:input={handleSearch}
			/>
		</div>
		<Button
			variant="outline"
			size="icon"
			on:click={() => (showAdvanced = !showAdvanced)}
			class={cn(showAdvanced && 'bg-primary/10')}
		>
			<SlidersHorizontal class="h-4 w-4" />
		</Button>
	</div>

	{#if showAdvanced}
		<div transition:slide class="flex flex-col gap-4">
			<div class="flex flex-wrap gap-4">
				<!-- Image Type Select -->
				<div class="flex flex-1 flex-col gap-2">
					<Label>Image Type</Label>
					<Select.Root selected={selectedImageType} onSelectedChange={onImageTypeSelect}>
						<Select.Trigger class="w-full">
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
				<div class="flex flex-1 flex-col gap-2">
					<Label>File Size</Label>
					<Select.Root selected={selectedSizeFilter} onSelectedChange={onSizeFilterSelect}>
						<Select.Trigger class="w-full">
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
				<div class="flex flex-1 flex-col gap-2">
					<Label>Sort By</Label>
					<Select.Root selected={selectedSortBy} onSelectedChange={onSortBySelect}>
						<Select.Trigger class="w-full">
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

			<!-- Action buttons -->
			<div class="flex justify-end gap-2">
				<Button variant="outline" on:click={handleReset}>Reset</Button>
				<Button on:click={applyFilters}>Apply Filters</Button>
			</div>
		</div>
	{/if}
</div>
