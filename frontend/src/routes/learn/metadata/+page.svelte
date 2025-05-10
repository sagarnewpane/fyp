<script>
	import { FileText, Lock, Eye, Settings } from 'lucide-svelte';
</script>

<div class="container mx-auto max-w-4xl px-4 py-8">
	<header class="mb-8">
		<div class="mb-4 flex items-center gap-3">
			<FileText class="h-8 w-8 text-primary" />
			<h1 class="text-3xl font-bold">Metadata Protection</h1>
		</div>
		<p class="text-xl text-muted-foreground">
			Learn how to secure sensitive image metadata and control what information is shared with others.
		</p>
	</header>

	<article class="prose prose-lg max-w-none">
		<section class="mb-8">
			<h2>What is Image Metadata?</h2>
			<p>
				Image metadata is the hidden information stored within your image files. This includes details like
				camera settings, location data, timestamps, and other technical information that can reveal sensitive
				details about your work and equipment.
			</p>
		</section>

		<section class="mb-8">
			<h2>Types of Metadata</h2>
			<div class="grid gap-6 md:grid-cols-2">
				<div class="rounded-lg border p-4">
					<FileText class="mb-2 h-6 w-6 text-primary" />
					<h3 class="text-xl font-semibold">EXIF Data</h3>
					<p>Camera settings, timestamps, and technical information.</p>
				</div>
				<div class="rounded-lg border p-4">
					<Eye class="mb-2 h-6 w-6 text-primary" />
					<h3 class="text-xl font-semibold">Location Data</h3>
					<p>GPS coordinates and location information.</p>
				</div>
				<div class="rounded-lg border p-4">
					<Settings class="mb-2 h-6 w-6 text-primary" />
					<h3 class="text-xl font-semibold">Custom Metadata</h3>
					<p>User-added information like copyright notices and descriptions.</p>
				</div>
			</div>
		</section>

		<section class="mb-8">
			<h2>How It Works</h2>
			<ol class="list-decimal pl-6">
				<li class="mb-4">
					<strong>Analyze Metadata</strong>
					<p>Scan your images for sensitive information in the metadata.</p>
				</li>
				<li class="mb-4">
					<strong>Select Protection Level</strong>
					<p>Choose what information to keep, modify, or remove.</p>
				</li>
				<li class="mb-4">
					<strong>Apply Protection</strong>
					<p>Process your images to implement the selected metadata protection.</p>
				</li>
			</ol>
		</section>

		<section class="mb-8">
			<h2>Best Practices</h2>
			<ul class="list-disc pl-6">
				<li>Regularly review and clean metadata before sharing images</li>
				<li>Keep copyright and attribution information while removing sensitive data</li>
				<li>Use different protection levels for different sharing scenarios</li>
				<li>Maintain a backup of original images with full metadata</li>
			</ul>
		</section>

		<section class="mb-8">
			<h2>Common Use Cases</h2>
			<div class="grid gap-4">
				<div class="rounded-lg border p-4">
					<h3 class="text-xl font-semibold">Professional Photography</h3>
					<p>Protect your shooting locations and equipment details.</p>
				</div>
				<div class="rounded-lg border p-4">
					<h3 class="text-xl font-semibold">Social Media Sharing</h3>
					<p>Remove sensitive metadata before posting images online.</p>
				</div>
				<div class="rounded-lg border p-4">
					<h3 class="text-xl font-semibold">Client Deliverables</h3>
					<p>Share images with appropriate metadata for client use.</p>
				</div>
			</div>
		</section>
	</article>
</div> 