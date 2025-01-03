<script>
	import { Search } from 'lucide-svelte';

	export let searchQuery = '';
</script>

<div class="flex items-center space-x-4">
	<div class="relative flex-1">
		<Search class="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-gray-400" />
		<input
			type="text"
			bind:value={searchQuery}
			placeholder="Search images..."
			class="w-full rounded-lg border border-gray-300 py-2 pl-10 pr-4 outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500"
		/>
	</div>
</div>
