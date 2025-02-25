<script>
	export let imageUrl = '';

	// Constants for image container dimensions
	const CONTAINER_WIDTH = 900;
	const CONTAINER_HEIGHT = 600;

	// State for image dimensions
	let imageDimensions = { width: CONTAINER_WIDTH, height: CONTAINER_HEIGHT };
	let imageLoaded = false;

	// Calculate optimal image dimensions
	function calculateImageDimensions(naturalWidth, naturalHeight) {
		if (!naturalWidth || !naturalHeight) return imageDimensions;

		const containerRatio = CONTAINER_WIDTH / CONTAINER_HEIGHT;
		const imageRatio = naturalWidth / naturalHeight;

		let width, height;

		if (imageRatio > containerRatio) {
			// Image is wider than container
			width = CONTAINER_WIDTH;
			height = Math.floor(CONTAINER_WIDTH / imageRatio);
		} else {
			// Image is taller than container
			height = CONTAINER_HEIGHT;
			width = Math.floor(CONTAINER_HEIGHT * imageRatio);
		}

		return { width, height };
	}

	// Handle image load event
	function handleImageLoad(event) {
		const img = event.target;
		imageDimensions = calculateImageDimensions(img.naturalWidth, img.naturalHeight);
		imageLoaded = true;
	}
</script>

<div
	class="relative h-full min-h-[600px] overflow-hidden rounded-lg border border-border bg-background"
>
	<div class="absolute inset-0 flex items-center justify-center">
		{#if imageUrl}
			<img
				src={imageUrl}
				alt="Preview"
				class="object-contain"
				on:load={handleImageLoad}
				style="width: {imageDimensions.width}px; height: {imageDimensions.height}px;"
			/>
		{:else}
			<div class="flex flex-col items-center text-muted-foreground">
				<svg class="mb-4 h-16 w-16" fill="none" stroke="currentColor" viewBox="0 0 24 24">
					<path
						stroke-linecap="round"
						stroke-linejoin="round"
						stroke-width="2"
						d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"
					/>
				</svg>
				<span>No image selected</span>
			</div>
		{/if}
	</div>

	{#if $$slots.default}
		<div class="absolute bottom-0 left-0 right-0 bg-background/80 p-4 backdrop-blur-sm">
			<slot />
		</div>
	{/if}
</div>

<style>
	img {
		max-width: 100%;
		max-height: 100%;
	}
</style>
