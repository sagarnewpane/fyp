<script lang="ts">
	import { LayoutDashboard, UserCog, Settings } from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';
	import { cn } from '$lib/utils';

	let { activeComponent = $bindable('overview') }: { activeComponent: string } = $props();

	// Navigation items
	const navItems = [
		{ id: 'overview', label: 'Overview', icon: LayoutDashboard },
		{ id: 'profile', label: 'Profile Management', icon: UserCog },
		{ id: 'settings', label: 'Settings', icon: Settings }
	];
</script>

<aside class="hidden w-64 space-y-4 border-r bg-card p-6 md:block">
	<div class="mb-8 flex items-center gap-2">
		<h1 class="text-xl font-bold">Dashboard</h1>
	</div>

	<nav class="space-y-2">
		{#each navItems as item}
			<Button
				variant="ghost"
				class={cn('w-full justify-start gap-2', activeComponent === item.id && 'bg-primary/10')}
				onclick={() => (activeComponent = item.id)}
			>
				<svelte:component this={item.icon} class="h-4 w-4" />
				{item.label}
			</Button>
		{/each}
	</nav>
</aside>
