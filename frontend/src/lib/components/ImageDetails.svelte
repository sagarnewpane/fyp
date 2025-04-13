<script>
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Badge } from '$lib/components/ui/badge';
	import {
		Image,
		FileText,
		Calendar,
		Layout,
		Shield,
		Circle,
		CheckCircle2,
		Clock
	} from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';
	export let imageInfo;

	// Function to format the string
	function formatString(input) {
		return input
			.split('_') // Split the string at underscores
			.map((word) => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()) // Capitalize each word
			.join(' '); // Join the words with a space
	}
</script>

<div class="w-full space-y-8">
	<div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
		<div class="space-y-1">
			<h2 class="text-2xl font-semibold tracking-tight text-foreground">
				Image Protection Details
			</h2>
			<p class="text-sm text-muted-foreground">Manage and view your protected image settings</p>
		</div>

		<!-- Add the logs button here -->
		<div class="flex items-center gap-2">
			<Button variant="default">
				<a href={`/logs/${imageInfo.id}`} class="flex items-center gap-2">
					<Clock class="h-4 w-4" />
					Access Logs
				</a>
			</Button>
		</div>
	</div>

	<div class="grid grid-cols-1 gap-8 md:grid-cols-2">
		<!-- Image Preview Card -->
		<Card class="overflow-hidden">
			<CardHeader class="border-b bg-muted/50 px-6 py-4">
				<CardTitle class="flex items-center gap-2 text-lg font-medium">
					<Image class="h-5 w-5" />
					Preview
				</CardTitle>
			</CardHeader>
			<CardContent class="p-0">
				<div class="group relative aspect-video w-full overflow-hidden bg-muted">
					<img
						src={imageInfo.image_url}
						alt={imageInfo.file_name}
						class="h-full w-full object-cover transition-all duration-300 hover:scale-105"
					/>
					<div
						class="absolute inset-0 bg-gradient-to-t from-black/40 to-transparent opacity-0 transition-opacity duration-300 group-hover:opacity-100"
					/>
					<div class="absolute bottom-4 right-4">
						<Badge variant="secondary" class="bg-black/50 text-white backdrop-blur-sm">
							Protected Image
						</Badge>
					</div>
				</div>
			</CardContent>
		</Card>

		<!-- Image Information Card -->
		<Card>
			<CardHeader class="border-b bg-muted/50 px-6 py-4">
				<CardTitle class="flex items-center gap-2 text-lg font-medium">
					<FileText class="h-5 w-5" />
					Image Information
				</CardTitle>
			</CardHeader>
			<CardContent class="p-6">
				<div class="space-y-6">
					<!-- File Details -->
					<div class="rounded-lg border bg-card p-4">
						<dl class="grid gap-4 text-sm">
							<div class="grid grid-cols-2 items-center gap-4">
								<dt class="font-medium text-muted-foreground">File Name</dt>
								<dd class="truncate font-medium">{imageInfo.image_name}</dd>
							</div>
							<div class="grid grid-cols-2 items-center gap-4">
								<dt class="font-medium text-muted-foreground">Size</dt>
								<dd class="font-medium">{imageInfo.file_size || 'N/A'}</dd>
							</div>
							<div class="grid grid-cols-2 items-center gap-4">
								<dt class="font-medium text-muted-foreground">Type</dt>
								<dd class="font-medium">{imageInfo.file_type.toUpperCase() || 'N/A'}</dd>
							</div>
							<div class="grid grid-cols-2 items-center gap-4">
								<dt class="font-medium text-muted-foreground">Upload Date</dt>
								<dd class="font-medium">
									{imageInfo.created_at}
								</dd>
							</div>
						</dl>
					</div>

					<!-- Protection Status -->
					<div class="rounded-lg border bg-card p-4">
						<h4 class="mb-4 font-medium">Protection Features</h4>
						<div class="grid gap-3">
							{#each Object.entries(imageInfo.security) as [key, value]}
								<div class="flex items-center justify-between rounded-md bg-muted/50 p-2.5">
									<div class="flex items-center gap-2">
										{#if value}
											<CheckCircle2 class="h-4 w-4 text-primary" />
										{:else}
											<Circle class="h-4 w-4 text-primary" />
										{/if}
										<span class="text-sm font-medium">{formatString(key)}</span>
									</div>
									<Badge variant={value ? 'default' : 'secondary'} class="ml-2">
										{value ? 'Applied' : 'Not Applied'}
									</Badge>
								</div>
							{/each}
						</div>
					</div>
				</div>
			</CardContent>
		</Card>
	</div>
</div>
