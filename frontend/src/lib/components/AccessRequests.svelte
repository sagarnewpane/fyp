<script>
	import {
		Card,
		CardContent,
		CardHeader,
		CardTitle,
		CardDescription
	} from '$lib/components/ui/card';
	import { Check, X, Clock } from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';
	import { Avatar, AvatarImage, AvatarFallback } from '$lib/components/ui/avatar';
	import { Badge } from '$lib/components/ui/badge';

	let requests = [
		{
			id: 1,
			user: 'John Doe',
			avatar: '',
			item: 'photo54.png',
			requestedAt: '10 minutes ago',
			message: 'Need access for project review'
		},
		{
			id: 2,
			user: 'Jane Smith',
			avatar: '',
			item: 'photo54.png',
			requestedAt: '2 hours ago',
			message: 'Would like to see the final version'
		}
	];
</script>

<Card>
	<CardHeader>
		<div class="flex items-center justify-between">
			<div>
				<CardTitle>Access Requests</CardTitle>
				<CardDescription>People waiting for your approval</CardDescription>
			</div>
			<Badge variant="secondary">{requests.length} pending</Badge>
		</div>
	</CardHeader>
	<CardContent>
		<div class="space-y-4">
			{#if requests.length === 0}
				<div class="flex flex-col items-center justify-center py-6 text-center">
					<div class="rounded-full bg-primary/10 p-3">
						<Check class="h-6 w-6 text-primary" />
					</div>
					<h3 class="mt-4 text-sm font-medium">All Clear!</h3>
					<p class="text-sm text-muted-foreground">No pending access requests</p>
				</div>
			{:else}
				{#each requests as request}
					<div class="group rounded-lg border p-4 transition-all hover:bg-muted/50">
						<div class="flex items-start justify-between gap-4">
							<div class="flex items-start space-x-4">
								<Avatar class="h-10 w-10 border-2 border-background">
									<AvatarImage src={request.avatar} alt={request.user} />
									<AvatarFallback class="font-medium">{request.user[0]}</AvatarFallback>
								</Avatar>
								<div class="space-y-1">
									<p class="text-sm font-medium leading-none">{request.user}</p>
									<div class="flex items-center gap-2">
										<Badge variant="secondary" class="font-normal">
											{request.item}
										</Badge>
									</div>
									<p class="text-sm text-muted-foreground">{request.message}</p>
									<div class="flex items-center gap-1 text-xs text-muted-foreground">
										<Clock class="h-3 w-3" />
										<span>{request.requestedAt}</span>
									</div>
								</div>
							</div>
							<div class="flex flex-col gap-2">
								<Button size="sm" variant="default" class="w-full">
									<Check class="mr-1 h-4 w-4" /> Approve
								</Button>
								<Button size="sm" variant="outline" class="w-full">
									<X class="mr-1 h-4 w-4" /> Deny
								</Button>
							</div>
						</div>
					</div>
				{/each}
			{/if}
		</div>
	</CardContent>
</Card>
