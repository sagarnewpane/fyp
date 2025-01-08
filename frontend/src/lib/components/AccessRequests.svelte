<script>
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Check, Trash2 } from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';
	import { Avatar, AvatarImage, AvatarFallback } from '$lib/components/ui/avatar';

	let requests = [
		{
			id: 1,
			user: 'John Doe',
			avatar: '$assets/ui-user.png',
			item: 'photo54.png'
		},
		{
			id: 2,
			user: 'Jane Smith',
			avatar: '$assets/ui-user.png',
			item: 'photo54.png'
		}
	];
</script>

<Card>
	<CardHeader>
		<CardTitle>Requested Access</CardTitle>
	</CardHeader>
	<CardContent>
		<div class="space-y-4">
			{#each requests as request}
				<div class="flex items-center justify-between space-x-4">
					<div class="flex items-center space-x-4">
						<Avatar>
							<AvatarImage src={request.avatar} alt={request.user} />
							<AvatarFallback>{request.user[0]}</AvatarFallback>
						</Avatar>
						<div>
							<p class="text-sm font-medium leading-none">{request.user}</p>
							<p class="text-sm text-muted-foreground">Requested access to {request.item}</p>
						</div>
					</div>
					<div class="flex space-x-2">
						<Button size="icon" variant="ghost">
							<Check class="h-4 w-4" />
						</Button>
						<Button size="icon" variant="ghost">
							<Trash2 class="h-4 w-4" />
						</Button>
					</div>
				</div>
			{/each}
		</div>
	</CardContent>
</Card>
