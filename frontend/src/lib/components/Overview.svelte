<script>
	import { onMount } from 'svelte';
	import {
		Eye,
		Download,
		Clock,
		UserPlus,
		X,
		Check,
		AlertCircle,
		Shield,
		Search,
		RefreshCw,
		Loader2
	} from 'lucide-svelte';
	import {
		Card,
		CardContent,
		CardHeader,
		CardTitle,
		CardDescription
	} from '$lib/components/ui/card';
	import { Avatar, AvatarImage, AvatarFallback } from '$lib/components/ui/avatar';
	import { Badge } from '$lib/components/ui/badge';
	import {
		Table,
		TableBody,
		TableCell,
		TableHead,
		TableHeader,
		TableRow
	} from '$lib/components/ui/table';
	import { Input } from '$lib/components/ui/input';
	import { Button } from '$lib/components/ui/button';
	import LogDetail from './LogDetail.svelte';
	import { toast } from 'svelte-sonner';

	let activityLogs = [];
	let isLoading = true;
	let error = null;
	let totalCount = 0;
	let searchQuery = '';

	let selectedLog = null;
	let showLogDialog = false;

	// Add new variables for requests
	let requests = [];
	let requestsLoading = true;
	let requestsError = null;
	let requestsCount = 0;
	let processing = {};

	function handleLogClick(log) {
		showLogDialog = false; // First close the dialog
		setTimeout(() => {
			// Then set new log and open dialog
			selectedLog = { ...log };
			showLogDialog = true;
		}, 0);
	}

	function handleDialogChange(isOpen) {
		showLogDialog = isOpen;
		if (!isOpen) {
			setTimeout(() => {
				// Clear selected log after dialog closes
				selectedLog = null;
			}, 100);
		}
	}

	async function fetchAccessLogs() {
		try {
			const response = await fetch('api/access-logs/', {
				headers: {
					'Content-Type': 'application/json'
				}
			});

			if (!response.ok) {
				throw new Error('Failed to fetch access logs');
			}

			const data = await response.json();
			activityLogs = data.results;
			totalCount = data.count;
		} catch (err) {
			error = err.message || 'An error occurred';
			console.error('Error fetching access logs:', err);
		} finally {
			isLoading = false;
		}
	}

	// Add requests fetching function
	async function fetchRequests() {
		requestsLoading = true;
		try {
			const response = await fetch('/api/access-requests');
			if (!response.ok) throw new Error('Failed to fetch requests');
			const data = await response.json();
			requests = data.results;
			requestsCount = data.count;
		} catch (err) {
			requestsError = err.message;
			toast.error('Failed to fetch requests');
		} finally {
			requestsLoading = false;
		}
	}

	// Add request handling function
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
			toast.success(`Request successful!`);
			await fetchRequests();
		} catch (err) {
			toast.error(err.message);
		} finally {
			processing[id] = null;
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

	function getActionIcon(action) {
		switch (action.toLowerCase()) {
			case 'view':
				return Eye;
			case 'attempt':
				return Clock;
			default:
				return Eye;
		}
	}

	onMount(() => {
		fetchAccessLogs();
		fetchRequests();
	});
</script>

<div class="container mx-auto max-w-7xl px-4 py-8">
	<div class="space-y-8">
		<div class="flex items-center justify-between">
			<h2 class="text-3xl font-bold tracking-tight">Activity Overview</h2>
			<div class="flex gap-4">
				<div class="relative w-[300px]">
					<Search class="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
					<Input placeholder="Search..." class="pl-8" bind:value={searchQuery} />
				</div>
				<Button
					variant="outline"
					on:click={() => {
						fetchAccessLogs();
						fetchRequests();
					}}>Refresh</Button
				>
			</div>
		</div>

		<!-- Pending Requests Section -->
		<Card>
			<CardHeader>
				<div class="flex items-center justify-between">
					<div>
						<CardTitle>Pending Access Requests</CardTitle>
						<CardDescription>Manage access requests for your protected images</CardDescription>
					</div>
					<Badge variant="secondary">{requestsCount} pending</Badge>
				</div>
			</CardHeader>
			<CardContent>
				<div class="max-h-[400px] space-y-2 overflow-y-auto pr-2">
					{#if requestsLoading}
						<div class="flex justify-center py-8">Loading...</div>
					{:else if requestsError}
						<div class="flex flex-col items-center py-8 text-center text-red-500">
							<AlertCircle class="mb-2 h-8 w-8" />
							<p>{requestsError}</p>
						</div>
					{:else if requests.length === 0}
						<div class="py-8 text-center text-muted-foreground">No pending requests</div>
					{:else}
						{#each requests as request}
							<div
								class="group flex items-start space-x-4 rounded-lg border p-4 transition-colors hover:bg-muted/50"
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
		</Card>

		<Card>
			<CardHeader>
				<CardTitle>Access Logs</CardTitle>
				<CardDescription
					>Track all access attempts and views of your protected images<br />
					<p class="mt-2 text-muted-foreground">Double click to view more details.</p>
				</CardDescription>
			</CardHeader>
			<CardContent>
				{#if isLoading}
					<div class="py-8 text-center">Loading...</div>
				{:else if error}
					<div class="py-8 text-center text-red-500">
						<AlertCircle class="mx-auto mb-2 h-8 w-8" />
						{error}
					</div>
				{:else if activityLogs.length === 0}
					<div class="py-8 text-center text-muted-foreground">No activity logs found</div>
				{:else}
					<div class="rounded-md border">
						<Table>
							<TableHeader>
								<TableRow class="group cursor-pointer hover:bg-muted/50">
									<TableHead class="w-[250px]">User</TableHead>
									<TableHead>Image</TableHead>
									<TableHead>Location</TableHead>
									<TableHead>Action</TableHead>
									<TableHead>Time</TableHead>
									<TableHead>Status</TableHead>
								</TableRow>
							</TableHeader>
							<TableBody>
								{#each activityLogs as log}
									<TableRow
										class="group cursor-pointer hover:bg-muted/50"
										on:click={() => handleLogClick(log)}
									>
										<TableCell>
											<div class="flex items-center gap-3">
												<Avatar class="h-8 w-8">
													<AvatarFallback>{log.email[0]}</AvatarFallback>
												</Avatar>
												<span class="text-sm font-medium leading-none">{log.email}</span>
											</div>
										</TableCell>
										<TableCell>
											<span class="text-sm font-medium">{log.image_name}</span>
										</TableCell>
										<TableCell>
											<span class="text-sm">{log.location}</span>
										</TableCell>
										<TableCell>
											<Badge
												variant="secondary"
												class="flex w-fit items-center gap-1 group-hover:bg-background"
											>
												<svelte:component this={getActionIcon(log.action_type)} class="h-3 w-3" />
												{log.action_type}
											</Badge>
										</TableCell>
										<TableCell>
											<div class="flex flex-col">
												<span class="text-sm">{formatTimeAgo(log.accessed_at)}</span>
												<span class="text-xs text-muted-foreground">
													{new Date(log.accessed_at).toLocaleDateString()}
												</span>
											</div>
										</TableCell>
										<TableCell>
											<Badge class="w-20 justify-center font-medium">
												{log.success ? 'Success' : 'Failed'}
											</Badge>
										</TableCell>
									</TableRow>
								{/each}
							</TableBody>
						</Table>
					</div>
				{/if}
			</CardContent>
		</Card>
	</div>
	<LogDetail log={selectedLog} open={showLogDialog} onOpenChange={handleDialogChange} />
</div>

<style>
	::-webkit-scrollbar {
		width: 6px;
	}

	::-webkit-scrollbar-track {
		background: transparent;
	}

	::-webkit-scrollbar-thumb {
		background: #ccc;
		border-radius: 3px;
	}
</style>
