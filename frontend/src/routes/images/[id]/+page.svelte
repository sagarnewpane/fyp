<script>
	import * as Alert from '$lib/components/ui/alert';
	import * as Card from '$lib/components/ui/card';
	import ImageDetails from '$lib/components/ImageDetails.svelte';
	import SecuritySettings from '$lib/components/SecuritySettings.svelte';

	// Svelte 4 reactive declaration
	export let data = null;

	// Reactive statements
	$: error = data?.error;
	$: imageData = data?.data;
</script>

{#if error}
	<div class="flex min-h-[200px] items-center justify-center">
		<Alert.Root variant="destructive" class="w-full max-w-md">
			<Alert.Title>Error</Alert.Title>
			<Alert.Description>{error}</Alert.Description>
		</Alert.Root>
	</div>
{:else if !imageData}
	<div class="flex min-h-[200px] items-center justify-center">
		<Alert.Root class="w-full max-w-md">
			<Alert.Title>Loading</Alert.Title>
			<Alert.Description>Please wait while the image loads...</Alert.Description>
		</Alert.Root>
	</div>
{:else}
	<main class="min-h-screen w-full bg-background">
		<div class="w-full space-y-8 px-4 py-6 md:px-6 lg:px-8">
			<ImageDetails imageInfo={imageData} />
			<SecuritySettings protectionStatus={imageData.security} />
		</div>
	</main>
{/if}
