<script>
	import {
		Card,
		CardContent,
		CardHeader,
		CardTitle,
		CardDescription,
		CardFooter
	} from '$lib/components/ui/card';
	import { Button } from '$lib/components/ui/button';
	import { Download, Image, Eye, Shield, Link2, ArrowRight } from 'lucide-svelte';
	import { Badge } from '$lib/components/ui/badge';

	let logs = [
		{
			id: 1,
			user: 'John Doe',
			action: 'Accessed',
			item: 'photo_23.png',
			time: '2 hours ago',
			icon: Eye,
			status: 'success'
		},
		{
			id: 2,
			user: 'Richard',
			action: 'Downloaded',
			item: 'watermarked photo2024.png',
			time: 'Yesterday',
			icon: Download,
			status: 'info'
		},
		{
			id: 3,
			user: 'System',
			action: 'Watermark Applied',
			item: 'photo2024.png',
			time: '3 days ago',
			icon: Shield,
			status: 'success'
		},
		{
			id: 4,
			user: 'Emma',
			action: 'Shared',
			item: 'family_photo.png',
			time: '4 days ago',
			icon: Link2,
			status: 'warning'
		},
		{
			id: 5,
			user: 'System',
			action: 'Backup Created',
			item: 'January Collection',
			time: '5 days ago',
			icon: Image,
			status: 'success'
		}
	];

	const getStatusColor = (status) => {
		const colors = {
			success: 'bg-green-100 text-green-700',
			warning: 'bg-yellow-100 text-yellow-700',
			info: 'bg-blue-100 text-blue-700',
			error: 'bg-red-100 text-red-700'
		};
		return colors[status] || colors.info;
	};
</script>

<Card>
	<CardHeader>
		<div class="flex items-center justify-between">
			<div>
				<CardTitle>Recent Activity</CardTitle>
				<CardDescription>Latest actions on your protected images</CardDescription>
			</div>
			<Badge variant="secondary" class="hidden sm:inline-flex">
				{logs.length} activities
			</Badge>
		</div>
	</CardHeader>
	<CardContent>
		<div class="space-y-5">
			{#each logs.slice(0, 3) as log}
				<div
					class="group flex items-start space-x-4 rounded-lg p-3 transition-colors hover:bg-muted/50"
				>
					<div class="rounded-full p-2 {getStatusColor(log.status)}">
						<svelte:component this={log.icon} class="h-4 w-4" />
					</div>
					<div class="flex-1 space-y-1">
						<div class="flex items-center justify-between">
							<p class="text-sm font-medium leading-none">
								<span class="font-semibold">{log.user}</span>
								<span class="text-muted-foreground"> {log.action}</span>
							</p>
							<time class="text-xs text-muted-foreground">{log.time}</time>
						</div>
						<p class="break-all text-sm text-muted-foreground">{log.item}</p>
					</div>
				</div>
			{/each}
		</div>
	</CardContent>
	<CardFooter>
		<Button variant="ghost" class="group w-full" size="sm">
			<span>View All Activities</span>
			<ArrowRight class="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
		</Button>
	</CardFooter>
</Card>
