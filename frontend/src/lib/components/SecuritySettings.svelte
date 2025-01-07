<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Badge } from '$lib/components/ui/badge';
	import { Shield, Fingerprint, FileText, Brain } from 'lucide-svelte';

	export let protectionStatus = {
		access_control: false,
		watermark: false,
		metadata: false,
		ai_protection: false
	};

	const securityFeatures = [
		{
			title: 'Access Controls',
			description: 'Control who can view and download your images with user-specific permissions.',
			icon: Shield,
			applied: protectionStatus.access_control,
			action: 'Manage Access'
		},
		{
			title: 'Watermarking Protection',
			description: 'Add visible watermarks to prevent unauthorized use and maintain copyright.',
			icon: Fingerprint,
			applied: protectionStatus.watermark,
			action: 'Apply Watermark'
		},
		{
			title: 'Metadata Protection',
			description: 'Secure sensitive image metadata and control what information is shared.',
			icon: FileText,
			applied: protectionStatus.metadata,
			action: 'Manage Metadata'
		},
		{
			title: 'AI Protection',
			description: 'Implement AI-based protection against unauthorized copying and manipulation.',
			icon: Brain,
			applied: protectionStatus.ai_protection,
			action: 'Apply Protection'
		}
	];
</script>

<section>
	<h2 class="mb-6 text-2xl font-semibold">Security Settings</h2>

	<div class="grid gap-6">
		{#each securityFeatures as feature}
			<Card>
				<CardHeader class="flex flex-row items-center justify-between space-y-0 pb-2">
					<CardTitle class="flex items-center gap-2 text-xl font-semibold">
						<svelte:component this={feature.icon} class="h-5 w-5" />
						{feature.title}
					</CardTitle>
					<Badge variant={feature.applied ? 'default' : 'secondary'}>
						{feature.applied ? 'Applied' : 'Not Applied'}
					</Badge>
				</CardHeader>
				<CardContent>
					<p class="mb-4 text-muted-foreground">{feature.description}</p>

					<div class="flex items-center justify-between">
						<Button variant="default">{feature.action}</Button>
						<Button variant="link" class="text-sm">Learn more</Button>
					</div>
				</CardContent>
			</Card>
		{/each}
	</div>
</section>
