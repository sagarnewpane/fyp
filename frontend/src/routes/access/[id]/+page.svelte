<script>
	import AccessControl from './AccessControl.svelte';
	export let data;
</script>

<!-- <ImageViewPage imageId="mock-image-id" /> -->
<div class="min-h-screen bg-background p-6">
	<div class="mx-auto max-w-[1400px]">
		<div class="mb-8">
			<h1 class="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl">Access Control</h1>
			<p class="mt-2 text-muted-foreground">
				Manage access settings and permissions for your image
			</p>
		</div>

		<AccessControl imageUrl={data.imageData.image_url} imageId={data.imageData.id} />
	</div>
</div>
