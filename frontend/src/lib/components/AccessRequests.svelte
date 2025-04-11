<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import {
		Card,
		CardContent,
		CardHeader,
		CardTitle,
		CardDescription,
		CardFooter
	} from '$lib/components/ui/card';
	import { Check, X, Clock, ArrowRight, RefreshCw, AlertCircle, Loader2 } from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';
	import { Badge } from '$lib/components/ui/badge';
	import { toast } from 'svelte-sonner';

	let requests = [];
	let isLoading = true;
	let error = null;
	let totalCount = 0;
	let processing = {};

	async function fetchRequests() {
		isLoading = true;
		try {
			const response = await fetch('/api/access-requests');
			if (!response.ok) throw new Error('Failed to fetch requests');
			const data = await response.json();
			requests = data.results;
			totalCount = data.count;
		} catch (err) {
			error = err.message;
			toast.error('Failed to fetch requests');
		} finally {
			isLoading = false;
		}
	}

	async function handleAction(id, action) {
		if (processing[id]) return;
		processing[id] = action;

		try {
			const response = await fetch(`/api/access-requests/${id}`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ action })
			});

			if (!response.ok) throw new Error(`Failed to ${action} request`);
			toast.success(`Request successfull!`);
			await fetchRequests();
		} catch (err) {
			toast.error(err.message);
		} finally {
			processing[id] = null;
		}
	}

	function handleViewAll() {
		goto('/user?tab=overview');
	}

	function formatTimeAgo(timestamp) {
		const date = new Date(timestamp);
		const now = new Date();
		const seconds = Math.floor((now - date) / 1000);

		if (seconds < 60) return 'just now';
		const minutes = Math.floor(seconds / 60);
		if (minutes < 60) return `${minutes} minutes ago`;
		const hours = Math.floor(minutes / 60);
		if (hours < 24) return `${hours} hours ago`;
		const days = Math.floor(hours / 24);
		return `${days} days ago`;
	}

	onMount(fetchRequests);
</script>

<Card class="flex h-[400px] flex-col">
	<CardHeader>
		<div class="flex items-center justify-between">
			<div>
				<CardTitle>Access Requests</CardTitle>
				<CardDescription>People waiting for your approval</CardDescription>
			</div>
			<div class="flex items-center gap-2">
				<Button variant="ghost" size="icon" on:click={fetchRequests} title="Refresh">
					<RefreshCw class="h-4 w-4" />
				</Button>
				<Badge variant="secondary" class="hidden sm:inline-flex">
					{totalCount} pending
				</Badge>
			</div>
		</div>
	</CardHeader>

	<CardContent class="flex-1">
		<div class="space-y-2">
			{#if isLoading}
				<div class="flex justify-center py-8">Loading...</div>
			{:else if error}
				<div class="flex flex-col items-center py-8 text-center text-red-500">
					<AlertCircle class="mb-2 h-8 w-8" />
					<p>{error}</p>
				</div>
			{:else if requests.length === 0}
				<div class="py-8 text-center text-muted-foreground">No pending requests</div>
			{:else}
				{#each requests.slice(0, 2) as request}
					<div
						class="group flex items-start space-x-4 rounded-lg px-3 py-2 transition-colors hover:bg-muted/50"
					>
						<div class="rounded-full bg-primary/10 p-2 text-primary">
							<Clock class="h-4 w-4" />
						</div>
						<div class="flex-1">
							<div class="flex items-center justify-between">
								<p class="text-sm font-medium leading-none">
									<span class="font-semibold">{request.email}</span>
									<span class="text-muted-foreground"> requested access</span>
								</p>
								<time class="text-xs text-muted-foreground">
									{formatTimeAgo(request.created_at)}
								</time>
							</div>
							<p class="mt-1 break-all text-sm text-muted-foreground">{request.image_name}</p>
							{#if request.message}
								<p class="mt-0.5 text-sm italic text-muted-foreground">{request.message}</p>
							{/if}
							<div class="mt-1.5 flex justify-end gap-2">
								<Button
									size="sm"
									variant="outline"
									class="h-8 min-w-[80px] bg-green-100 text-green-700 hover:bg-green-200"
									disabled={!!processing[request.id]}
									on:click={() => handleAction(request.id, 'approve')}
								>
									{#if processing[request.id] === 'approve'}
										<Loader2 class="mr-1.5 h-3.5 w-3.5 animate-spin" />
									{:else}
										<Check class="mr-1.5 h-3.5 w-3.5" />
									{/if}
									Approve
								</Button>
								<Button
									size="sm"
									variant="outline"
									class="h-8 min-w-[80px] bg-red-100 text-red-700 hover:bg-red-200"
									disabled={!!processing[request.id]}
									on:click={() => handleAction(request.id, 'deny')}
								>
									{#if processing[request.id] === 'deny'}
										<Loader2 class="mr-1.5 h-3.5 w-3.5 animate-spin" />
									{:else}
										<X class="mr-1.5 h-3.5 w-3.5" />
									{/if}
									Deny
								</Button>
							</div>
						</div>
					</div>
				{/each}
			{/if}
		</div>
	</CardContent>

	<CardFooter class="flex justify-end pb-4">
		<Button variant="default" class="group" on:click={handleViewAll}>
			<span>View All Activities</span>
			<ArrowRight class="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
		</Button>
	</CardFooter>
</Card>
