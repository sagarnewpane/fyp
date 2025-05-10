<script>
	import WatermarkEditor from '$lib/components/WatermarkEditor.svelte';
	import { Alert, AlertDescription } from '$lib/components/ui/alert';

	export let data;
</script>

<main class="min-h-screen w-full bg-background p-6 text-foreground">
	<div class="mx-auto max-w-6xl space-y-6">
		<!-- <h1 class="text-3xl font-bold">Image Watermarking Tool</h1> -->
		<!-- <p class="text-muted-foreground">Apply watermark to your image</p> -->

		{#if data.error}
			<Alert variant="destructive">
				<AlertDescription>{data.error}</AlertDescription>
			</Alert>
		{:else}
			<WatermarkEditor
				imageUrl={data.imageData.image_url}
				imageId={data.imageData.id}
				initialSettings={data.settings}
			/>
		{/if}
	</div>
</main>
