<script>
	export let totalPages = 1;
	export let currentPage = 1;
	export let onPageChange;

	// Generate an array of page numbers to display
	$: visiblePages = getVisiblePages(currentPage, totalPages);

	function getVisiblePages(current, total) {
		if (total <= 7) return Array.from({ length: total }, (_, i) => i + 1);

		if (current <= 4) {
			return [1, 2, 3, 4, 5, '...', total];
		}

		if (current >= total - 3) {
			return [1, '...', total - 4, total - 3, total - 2, total - 1, total];
		}

		return [1, '...', current - 1, current, current + 1, '...', total];
	}
</script>

<nav class="flex items-center justify-center gap-2" aria-label="Pagination">
	<button
		class="inline-flex items-center justify-center rounded-md border border-input bg-background px-4 py-2 text-sm font-medium
               transition-colors hover:bg-accent hover:text-accent-foreground
               focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary
               disabled:pointer-events-none disabled:opacity-50"
		disabled={currentPage === 1}
		on:click={() => onPageChange(currentPage - 1)}
		aria-label="Go to previous page"
	>
		<svg class="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
			<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
		</svg>
		Previous
	</button>

	<div class="flex gap-1">
		{#each visiblePages as page}
			{#if page === '...'}
				<span class="flex h-10 w-10 items-center justify-center text-sm text-muted-foreground">
					{page}
				</span>
			{:else}
				<button
					class="inline-flex h-10 w-10 items-center justify-center rounded-md text-sm transition-colors
                           {currentPage === page
						? 'bg-primary text-primary-foreground hover:bg-primary/90'
						: 'border border-input bg-background hover:bg-accent hover:text-accent-foreground'}
                           focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
					on:click={() => onPageChange(page)}
					aria-label="Go to page {page}"
					aria-current={currentPage === page ? 'page' : undefined}
				>
					{page}
				</button>
			{/if}
		{/each}
	</div>

	<button
		class="inline-flex items-center justify-center rounded-md border border-input bg-background px-4 py-2 text-sm font-medium
               transition-colors hover:bg-accent hover:text-accent-foreground
               focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary
               disabled:pointer-events-none disabled:opacity-50"
		disabled={currentPage === totalPages}
		on:click={() => onPageChange(currentPage + 1)}
		aria-label="Go to next page"
	>
		Next
		<svg class="ml-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
			<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
		</svg>
	</button>
</nav>
