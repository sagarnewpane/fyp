<script lang="js">
	import Sidebar from '$lib/components/Sidebar.svelte';
	import Overview from '$lib/components/Overview.svelte';
	import ProfileManagement from '$lib/components/ProfileManagement.svelte';
	import Settings from '$lib/components/Settings.svelte';
	import { page } from '$app/stores';

	// Check URL query parameter for initial tab
	$: activeComponent = $page.url.searchParams.get('tab') || 'overview';
</script>

<div class="flex min-h-screen w-full bg-background">
	<Sidebar bind:activeComponent />

	<main class="flex-1 space-y-8 overflow-y-auto p-6 md:p-8">
		{#if activeComponent === 'overview'}
			<Overview />
		{:else if activeComponent === 'profile'}
			<ProfileManagement />
		{:else if activeComponent === 'settings'}
			<Settings />
		{/if}
	</main>
</div>
