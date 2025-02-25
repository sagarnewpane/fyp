<script>
	import AccessControl from './AccessControl.svelte';
	export let data;
</script>

<main class="min-h-screen w-full bg-background p-6 text-foreground">
	<div class="mx-auto space-y-6">
		<h1 class="text-3xl font-bold">Image Watermarking Tool</h1>

		<AccessControl
			imageUrl={data.imageData.image_url}
			imageId={data.imageData.id}
			imageSecurity={data.imageData.security}
		/>
	</div>
</main>
