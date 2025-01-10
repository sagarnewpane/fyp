<script lang="ts">
	import { Eye, Download, Clock, UserPlus, X, Check, AlertCircle } from 'lucide-svelte';
	import {
		Card,
		CardContent,
		CardHeader,
		CardTitle,
		CardDescription
	} from '$lib/components/ui/card';
	import { Avatar, AvatarImage, AvatarFallback } from '$lib/components/ui/avatar';
	import { Button } from '$lib/components/ui/button';
	import { Badge } from '$lib/components/ui/badge';
	import {
		Table,
		TableBody,
		TableCell,
		TableHead,
		TableHeader,
		TableRow
	} from '$lib/components/ui/table';

	// Pending access requests
	const accessRequests = [
		{
			user: 'Alice Johnson',
			email: 'alice@example.com',
			images: ['vacation_2024.jpg', 'family_photo.jpg'],
			requestedAt: '2 hours ago',
			message: 'Would like to view these family photos'
		},
		{
			user: 'Bob Smith',
			email: 'bob@example.com',
			images: ['project_preview.png'],
			requestedAt: 'Yesterday',
			message: 'Need access for the client project'
		}
	];

	// Recent activity logs
	const activityLogs = [
		{
			user: 'Emma Wilson',
			action: 'downloaded',
			image: 'team_photo.jpg',
			timestamp: '10 minutes ago',
			status: 'success'
		},
		{
			user: 'David Chen',
			action: 'requested access',
			image: 'design_mockup.png',
			timestamp: '1 hour ago',
			status: 'pending'
		},
		{
			user: 'Sarah Miller',
			action: 'viewed',
			image: 'presentation.jpg',
			timestamp: '3 hours ago',
			status: 'success'
		},
		{
			user: 'James Brown',
			action: 'was denied access',
			image: 'confidential.pdf',
			timestamp: '5 hours ago',
			status: 'denied'
		}
	];

	function handleApprove(request: any) {
		// Implement approve logic
	}

	function handleDeny(request: any) {
		// Implement deny logic
	}
</script>

<div class="container mx-auto max-w-6xl px-4 py-8">
	<div class="space-y-8">
		<div>
			<h2 class="text-3xl font-bold tracking-tight">Activity Overview</h2>
			<p class="mt-2 text-muted-foreground">Monitor access requests and recent activities</p>
		</div>

		<!-- Pending Access Requests -->
		<Card>
			<CardHeader>
				<div class="flex items-center justify-between">
					<div>
						<CardTitle>Pending Access Requests</CardTitle>
						<CardDescription
							>Review and manage access requests for your protected images</CardDescription
						>
					</div>
					<Badge variant="secondary">{accessRequests.length} Pending</Badge>
				</div>
			</CardHeader>
			<CardContent>
				<div class="space-y-6">
					{#if accessRequests.length === 0}
						<div class="py-6 text-center text-muted-foreground">No pending access requests</div>
					{:else}
						{#each accessRequests as request}
							<div class="flex items-start justify-between rounded-lg border p-4">
								<div class="flex gap-4">
									<Avatar>
										<AvatarImage
											src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${request.user}`}
											alt={request.user}
										/>
										<AvatarFallback>{request.user[0]}</AvatarFallback>
									</Avatar>
									<div class="space-y-1">
										<p class="font-medium">{request.user}</p>
										<p class="text-sm text-muted-foreground">{request.email}</p>
										<p class="text-sm">{request.message}</p>
										<div class="mt-2 flex gap-2">
											{#each request.images as image}
												<Badge variant="secondary">{image}</Badge>
											{/each}
										</div>
									</div>
								</div>
								<div class="ml-4 flex flex-col gap-2">
									<Button size="sm" class="w-24" on:click={() => handleApprove(request)}>
										<Check class="mr-1 h-4 w-4" /> Approve
									</Button>
									<Button
										size="sm"
										variant="outline"
										class="w-24"
										on:click={() => handleDeny(request)}
									>
										<X class="mr-1 h-4 w-4" /> Deny
									</Button>
								</div>
							</div>
						{/each}
					{/if}
				</div>
			</CardContent>
		</Card>

		<!-- Activity Log -->
		<Card>
			<CardHeader>
				<CardTitle>Recent Activity</CardTitle>
				<CardDescription>Track all activities related to your protected images</CardDescription>
			</CardHeader>
			<CardContent>
				<Table>
					<TableHeader>
						<TableRow>
							<TableHead>User</TableHead>
							<TableHead>Activity</TableHead>
							<TableHead>Image</TableHead>
							<TableHead>Time</TableHead>
							<TableHead>Status</TableHead>
						</TableRow>
					</TableHeader>
					<TableBody>
						{#each activityLogs as log}
							<TableRow>
								<TableCell>
									<div class="flex items-center gap-2">
										<Avatar class="h-8 w-8">
											<AvatarImage
												src={`https://api.dicebear.com/7.x/avataaars/svg?seed=${log.user}`}
												alt={log.user}
											/>
											<AvatarFallback>{log.user[0]}</AvatarFallback>
										</Avatar>
										<span>{log.user}</span>
									</div>
								</TableCell>
								<TableCell>{log.action}</TableCell>
								<TableCell>{log.image}</TableCell>
								<TableCell>{log.timestamp}</TableCell>
								<TableCell>
									<Badge
										variant={log.status === 'success'
											? 'success'
											: log.status === 'pending'
												? 'warning'
												: 'destructive'}
									>
										{log.status}
									</Badge>
								</TableCell>
							</TableRow>
						{/each}
					</TableBody>
				</Table>
			</CardContent>
		</Card>
	</div>
</div>
