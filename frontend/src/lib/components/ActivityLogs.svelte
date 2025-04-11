<script>
	import { onMount } from 'svelte';
	import {
		Card,
		CardContent,
		CardHeader,
		CardTitle,
		CardDescription,
		CardFooter
	} from '$lib/components/ui/card';
	import { Button } from '$lib/components/ui/button';
	import {
		Download,
		Image,
		Eye,
		Shield,
		Link2,
		ArrowRight,
		AlertCircle,
		RefreshCw,
		Clock
	} from 'lucide-svelte';
	import { Badge } from '$lib/components/ui/badge';
	import { goto } from '$app/navigation';

	let activityLogs = [];
	let isLoading = true;
	let error = null;
	let totalCount = 0;

	async function fetchAccessLogs() {
		isLoading = true;
		try {
			const response = await fetch('/api/access-logs/', {
				headers: {
					'Content-Type': 'application/json'
				}
			});

			if (!response.ok) {
				throw new Error('Failed to fetch access logs');
			}

			const data = await response.json();
			console.log(data);
			activityLogs = data.results;
			totalCount = data.count;
		} catch (err) {
			error = err.message || 'An error occurred';
			console.error('Error fetching access logs:', err);
		} finally {
			isLoading = false;
		}
	}

	function getActionIcon(action) {
		switch (action.toLowerCase()) {
			case 'view':
				return Eye;
			case 'download':
				return Download;
			case 'watermark':
				return Shield;
			case 'share':
				return Link2;
			case 'upload':
				return Image;
			case 'attempt':
				return Clock;
			default:
				return Eye;
		}
	}

	function formatTimeAgo(timestamp) {
		const date = new Date(timestamp);
		const now = new Date();
		const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);

		if (seconds < 60) return 'just now';
		const minutes = Math.floor(seconds / 60);
		if (minutes < 60) return `${minutes} minutes ago`;
		const hours = Math.floor(minutes / 60);
		if (hours < 24) return `${hours} hours ago`;
		const days = Math.floor(hours / 24);
		return `${days} days ago`;
	}

	function navigateToAllLogs() {
		goto('/user?tab=overview');
	}

	onMount(() => {
		fetchAccessLogs();
	});
</script>

<Card class="flex h-[400px] flex-col">
	<CardHeader>
		<div class="flex items-center justify-between">
			<div>
				<CardTitle>Recent Activity</CardTitle>
				<CardDescription>Latest actions on your protected images</CardDescription>
			</div>
			<div class="flex items-center gap-2">
				<Button variant="ghost" size="icon" on:click={fetchAccessLogs} title="Refresh">
					<RefreshCw class="h-4 w-4" />
				</Button>
				<Badge variant="secondary" class="hidden sm:inline-flex">
					{totalCount} activities
				</Badge>
			</div>
		</div>
	</CardHeader>
	<CardContent class="flex-1">
		<div class="space-y-5">
			{#if isLoading}
				<div class="flex justify-center py-8">Loading...</div>
			{:else if error}
				<div class="flex flex-col items-center py-8 text-center text-red-500">
					<AlertCircle class="mb-2 h-8 w-8" />
					<p>{error}</p>
				</div>
			{:else if activityLogs.length === 0}
				<div class="py-8 text-center text-muted-foreground">No activity logs found</div>
			{:else}
				{#each activityLogs.slice(0, 3) as log}
					<div
						class="group flex items-start space-x-4 rounded-lg p-3 transition-colors hover:bg-muted/50"
					>
						<div
							class="rounded-full p-2 {log.success
								? 'bg-green-100 text-green-700'
								: 'bg-red-100 text-red-700'}"
						>
							<svelte:component this={getActionIcon(log.action_type)} class="h-4 w-4" />
						</div>
						<div class="flex-1 space-y-1">
							<div class="flex items-center justify-between">
								<p class="text-sm font-medium leading-none">
									<span class="font-semibold">{log.email}</span>
									<span class="text-muted-foreground"> {log.action_type}</span>
								</p>
								<time class="text-xs text-muted-foreground">{formatTimeAgo(log.accessed_at)}</time>
							</div>
							<p class="break-all text-sm text-muted-foreground">{log.image_name}</p>
						</div>
					</div>
				{/each}
			{/if}
		</div>
	</CardContent>
	<CardFooter class="flex justify-end pb-4">
		<Button variant="default" class="group" on:click={navigateToAllLogs}>
			<span>View All Activities</span>
			<ArrowRight class="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
		</Button>
	</CardFooter>
</Card>
