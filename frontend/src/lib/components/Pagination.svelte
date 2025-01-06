<script>
	export let totalPages = 1;
	export let currentPage = 1;
	export let onPageChange;

	$: pages = Array.from({ length: totalPages }, (_, i) => i + 1);
</script>

<div class="flex items-center justify-center gap-2">
	<button
		class="rounded border px-3 py-1 {currentPage === 1
			? 'cursor-not-allowed bg-gray-100'
			: 'hover:bg-gray-50'}"
		disabled={currentPage === 1}
		on:click={() => onPageChange(currentPage - 1)}
	>
		Previous
	</button>

	{#each pages as page}
		<button
			class="rounded border px-3 py-1 {currentPage === page
				? 'bg-blue-500 text-white'
				: 'hover:bg-gray-50'}"
			on:click={() => onPageChange(page)}
		>
			{page}
		</button>
	{/each}

	<button
		class="rounded border px-3 py-1 {currentPage === totalPages
			? 'cursor-not-allowed bg-gray-100'
			: 'hover:bg-gray-50'}"
		disabled={currentPage === totalPages}
		on:click={() => onPageChange(currentPage + 1)}
	>
		Next
	</button>
</div>
