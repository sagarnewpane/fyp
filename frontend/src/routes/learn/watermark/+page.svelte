<script>
	import { Fingerprint, Image, Settings, Shield } from 'lucide-svelte';
</script>

<div class="container mx-auto max-w-4xl px-4 py-8">
	<header class="mb-8">
		<div class="mb-4 flex items-center gap-3">
			<Fingerprint class="h-8 w-8 text-primary" />
			<h1 class="text-3xl font-bold">Watermarking Protection</h1>
		</div>
		<p class="text-xl text-muted-foreground">
			Learn how to protect your images with professional watermarking techniques and maintain your copyright.
		</p>
	</header>

	<article class="prose prose-lg max-w-none">
		<section class="mb-8">
			<h2>What is Image Watermarking?</h2>
			<p>
				Image watermarking is a technique that embeds a visible or invisible mark on your images to protect
				your intellectual property. It helps deter unauthorized use while maintaining the visual quality of
				your work.
			</p>
		</section>

		<section class="mb-8">
			<h2>Types of Watermarks</h2>
			<div class="grid gap-6 md:grid-cols-2">
				<div class="rounded-lg border p-4">
					<Image class="mb-2 h-6 w-6 text-primary" />
					<h3 class="text-xl font-semibold">Visible Watermarks</h3>
					<p>Text or logo overlays that are clearly visible on the image.</p>
				</div>
				<div class="rounded-lg border p-4">
					<Shield class="mb-2 h-6 w-6 text-primary" />
					<h3 class="text-xl font-semibold">Invisible Watermarks</h3>
					<p>Digital signatures embedded in the image data that are not visible to the naked eye.</p>
				</div>
				<div class="rounded-lg border p-4">
					<Settings class="mb-2 h-6 w-6 text-primary" />
					<h3 class="text-xl font-semibold">Customizable Options</h3>
					<p>Adjust opacity, position, size, and style to match your branding.</p>
				</div>
			</div>
		</section>

		<section class="mb-8">
			<h2>How It Works</h2>
			<ol class="list-decimal pl-6">
				<li class="mb-4">
					<strong>Choose Watermark Type</strong>
					<p>Select between visible or invisible watermarking based on your needs.</p>
				</li>
				<li class="mb-4">
					<strong>Customize Your Watermark</strong>
					<p>Add your logo, text, or digital signature with customizable settings.</p>
				</li>
				<li class="mb-4">
					<strong>Apply Protection</strong>
					<p>Process your images with the selected watermark settings.</p>
				</li>
			</ol>
		</section>

		<section class="mb-8">
			<h2>Best Practices</h2>
			<ul class="list-disc pl-6">
				<li>Keep watermarks visible but not intrusive</li>
				<li>Use consistent branding across all watermarked images</li>
				<li>Consider using both visible and invisible watermarks for maximum protection</li>
				<li>Regularly update your watermark design to stay current</li>
			</ul>
		</section>

		<section class="mb-8">
			<h2>Common Use Cases</h2>
			<div class="grid gap-4">
				<div class="rounded-lg border p-4">
					<h3 class="text-xl font-semibold">Photography Portfolios</h3>
					<p>Protect your work while showcasing it to potential clients.</p>
				</div>
				<div class="rounded-lg border p-4">
					<h3 class="text-xl font-semibold">Stock Photography</h3>
					<p>Share preview images with watermarks before purchase.</p>
				</div>
				<div class="rounded-lg border p-4">
					<h3 class="text-xl font-semibold">Digital Art</h3>
					<p>Protect your digital artwork from unauthorized use.</p>
				</div>
			</div>
		</section>
	</article>
</div> 