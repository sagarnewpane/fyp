<script>
	import { Card, CardContent, CardHeader, CardTitle, CardFooter } from '$lib/components/ui/card';
	import { Button } from '$lib/components/ui/button';
	import { Download, Image, Eye, Shield, Link2 } from 'lucide-svelte';

	let logs = [
		{
			id: 1,
			user: 'John Doe',
			action: 'Accessed',
			item: 'photo_23.png',
			time: '2 hours ago',
			icon: Eye
		},
		{
			id: 2,
			user: 'Richard',
			action: 'Downloaded',
			item: 'watermarked photo2024.png',
			time: 'Yesterday',
			icon: Download
		},
		{
			id: 3,
			user: 'System',
			action: 'Watermark Applied',
			item: 'photo2024.png',
			time: '3 days ago',
			icon: Shield
		},
		{
			id: 4,
			user: 'Emma',
			action: 'Shared',
			item: 'family_photo.png',
			time: '4 days ago',
			icon: Link2
		},
		{
			id: 5,
			user: 'System',
			action: 'Backup Created',
			item: 'January Collection',
			time: '5 days ago',
			icon: Image
		}
	];
</script>

<Card>
	<CardHeader>
		<CardTitle>Recent Logs</CardTitle>
	</CardHeader>
	<CardContent>
		<div class="space-y-4">
			{#each logs.slice(0, 3) as log}
				<div class="flex items-start space-x-4 border-b pb-4 last:border-0 last:pb-0">
					<div class="rounded-full bg-primary/10 p-2">
						<svelte:component this={log.icon} class="h-4 w-4 text-primary" />
					</div>
					<div class="flex-1">
						<p class="text-sm font-medium">{log.user} {log.action}</p>
						<p class="text-sm text-muted-foreground">{log.item}</p>
					</div>
					<span class="text-xs text-muted-foreground">{log.time}</span>
				</div>
			{/each}
		</div>
	</CardContent>
	<CardFooter>
		<Button variant="ghost" class="w-full">View All Logs</Button>
	</CardFooter>
</Card>
