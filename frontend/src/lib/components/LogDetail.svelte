<script>
	import {
		Dialog,
		DialogContent,
		DialogHeader,
		DialogTitle,
		DialogDescription
	} from '$lib/components/ui/dialog';
	import { Badge } from '$lib/components/ui/badge';
	import { Shield, MapPin, Globe, Clock, User, Image } from 'lucide-svelte';

	export let log = null;
	export let open = false;
	export let onOpenChange = () => {};

	$: formattedDate = log ? new Date(log.accessed_at).toLocaleString() : '';
</script>

<Dialog {open} {onOpenChange}>
	<DialogContent class="max-w-2xl">
		<DialogHeader>
			<DialogTitle>Access Log Details</DialogTitle>
			<DialogDescription>Detailed information about this access event</DialogDescription>
		</DialogHeader>

		{#if log}
			<div class="grid gap-4">
				<!-- Status Badge -->
				<div class="flex justify-end">
					<Badge variant={log.success ? 'success' : 'destructive'} class="w-24 justify-center">
						{log.success ? 'Success' : 'Failed'}
					</Badge>
				</div>

				<!-- Main Info Grid -->
				<div class="grid grid-cols-2 gap-4">
					<!-- User Information -->
					<div class="space-y-2">
						<h4 class="flex items-center gap-2 font-semibold">
							<User class="h-4 w-4" />
							User Information
						</h4>
						<div class="space-y-1">
							<p class="text-sm">Email: {log.email}</p>
							<p class="text-sm">IP Address: {log.ip_address}</p>
						</div>
					</div>

					<!-- Image Information -->
					<div class="space-y-2">
						<h4 class="flex items-center gap-2 font-semibold">
							<Image class="h-4 w-4" />
							Image Details
						</h4>
						<div class="space-y-1">
							<p class="text-sm">Name: {log.image_name}</p>
							<p class="text-sm">ID: {log.image_id}</p>
						</div>
					</div>

					<!-- Location Information -->
					<div class="space-y-2">
						<h4 class="flex items-center gap-2 font-semibold">
							<MapPin class="h-4 w-4" />
							Location Details
						</h4>
						<div class="space-y-1">
							<p class="text-sm">Location: {log.location}</p>
							<p class="text-sm">Browser: {log.user_agent || 'Unknown'}</p>
						</div>
					</div>

					<!-- Time Information -->
					<div class="space-y-2">
						<h4 class="flex items-center gap-2 font-semibold">
							<Clock class="h-4 w-4" />
							Timing
						</h4>
						<div class="space-y-1">
							<p class="text-sm">Accessed: {formattedDate}</p>
						</div>
					</div>
				</div>

				<!-- Protection Features -->
				<div class="space-y-2">
					<h4 class="flex items-center gap-2 font-semibold">
						<Shield class="h-4 w-4" />
						Protection Features
					</h4>
					<div class="flex flex-wrap gap-2">
						{#if Object.values(log.protection_features).some((v) => v)}
							{#each Object.entries(log.protection_features) as [key, enabled]}
								{#if enabled}
									<Badge variant="outline">
										{key.replace('_', ' ')}
									</Badge>
								{/if}
							{/each}
						{:else}
							<span class="text-sm text-muted-foreground">No protection features enabled</span>
						{/if}
					</div>
				</div>
			</div>
		{/if}
	</DialogContent>
</Dialog>
