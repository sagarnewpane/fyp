<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Badge } from '$lib/components/ui/badge';
	import { Shield, Fingerprint, FileText, Brain } from 'lucide-svelte';

	export let protectionStatus = {
		access_control: false,
		watermark: false,
		metadata: false,
		ai_protection: false
	};
	export let imageId;

	const securityFeatures = [
		{
			title: 'Access Controls',
			description: 'Control who can view and download your images with user-specific permissions.',
			icon: Shield,
			applied: protectionStatus.access_control,
			action: 'Manage Access',
			url: `/access/${imageId}`,
			image: '/features/access.png'
		},
		{
			title: 'Watermarking Protection',
			description: 'Add visible watermarks to prevent unauthorized use and maintain copyright.',
			icon: Fingerprint,
			applied: protectionStatus.watermark,
			action: 'Apply Watermark',
			url: `/watermark/${imageId}`,
			image: '/features/watermark.png'
		},
		{
			title: 'Metadata Protection',
			description: 'Secure sensitive image metadata and control what information is shared.',
			icon: FileText,
			applied: protectionStatus.metadata,
			action: 'Manage Metadata',
			url: `/metadata/${imageId}`,
			image: '/features/metadata.png'
		},
		{
			title: 'AI Protection',
			description: 'Implement AI-based protection against unauthorized copying and manipulation.',
			icon: Brain,
			applied: protectionStatus.ai_protection,
			action: 'Apply Protection',
			url: `/ai-protection/${imageId}`,
			image: '/features/ai.png'
		}
	];
</script>

<section>
	<h2 class="mb-6 text-2xl font-semibold">Security Settings</h2>

	<div class="grid grid-cols-1 gap-6 md:grid-cols-2">
		{#each securityFeatures as feature}
			<div
				class="security-box flex h-80 overflow-hidden rounded-lg border shadow-md transition-all duration-300 hover:border-primary/50 hover:shadow-lg"
			>
				<!-- Content on left -->
				<div class="flex flex-1 flex-col justify-between p-5">
					<div>
						<div class="mb-2 flex items-center justify-between">
							<h3 class="flex items-center gap-2 text-xl font-semibold">
								<svelte:component this={feature.icon} class="h-6 w-6 text-primary" />
								{feature.title}
							</h3>
							<Badge variant={feature.applied ? 'default' : 'secondary'} class="ml-2">
								{feature.applied ? 'Applied' : 'Not Applied'}
							</Badge>
						</div>

						<p class="mb-4 text-muted-foreground">{feature.description}</p>
					</div>

					<div class="flex items-center">
						<Button href={feature.url} variant="default" class="mr-3">{feature.action}</Button>
						<Button variant="outline" size="sm">Learn more</Button>
					</div>
				</div>

				<!-- Image on right -->
				<div class="relative w-1/2 flex-shrink-0 overflow-hidden">
					{#if feature.image}
						<img
							src={feature.image}
							alt={feature.title}
							class="h-full w-full object-cover transition-transform duration-300 hover:scale-105"
						/>
					{:else}
						<div class="flex h-full w-full items-center justify-center bg-gray-100">
							<svelte:component this={feature.icon} class="h-16 w-16 text-gray-300" />
						</div>
					{/if}
				</div>
			</div>
		{/each}
	</div>
</section>

<style>
	.security-box {
		background-color: white;
	}
</style>
