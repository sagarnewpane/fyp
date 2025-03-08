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
		Search
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

	let activityLogs = [];
	let isLoading = true;
	let error = null;
	let totalCount = 0;
	let searchQuery = '';

	let selectedLog = null;
	let showLogDialog = false;

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
	});
</script>

<div class="container mx-auto max-w-7xl px-4 py-8">
	<div class="space-y-8">
		<div class="flex items-center justify-between">
			<div>
				<h2 class="text-3xl font-bold tracking-tight">Activity Overview</h2>
				<p class="mt-2 text-muted-foreground">
					Monitor access activity for your protected images ({totalCount} total events)
				</p>
			</div>
			<div class="flex gap-4">
				<div class="relative w-[300px]">
					<Search class="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
					<Input placeholder="Search logs..." class="pl-8" bind:value={searchQuery} />
				</div>
				<Button variant="outline" on:click={fetchAccessLogs}>Refresh</Button>
			</div>
		</div>

		<Card>
			<CardHeader>
				<CardTitle>Access Logs</CardTitle>
				<CardDescription
					>Track all access attempts and views of your protected images<br />
					<p class="mt-2 text-muted-foreground">Double click to view more detials.</p>
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
