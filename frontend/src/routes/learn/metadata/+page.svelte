<script>
	import { FileText, Lock, Eye, Settings } from 'lucide-svelte';
</script>

<div class="w-full bg-white text-gray-800 py-16 px-6 lg:px-24">
	<article class="max-w-screen-xl mx-auto space-y-16">
		<!-- Hero Header -->
		<header class="text-center">
			<div class="flex justify-center mb-4">
				<FileText class="h-10 w-10 text-primary" />
			</div>
			<h1 class="text-4xl sm:text-5xl font-extrabold mb-4">Metadata Protection: Guard Your Digital Footprint</h1>
			<p class="text-xl text-gray-600 max-w-2xl mx-auto">
				Every image carries hidden information that could reveal more than you intend. Learn how to control what metadata stays with your images and what gets removed.
			</p>
		</header>

		<!-- Intro Section -->
		<section class="grid md:grid-cols-2 gap-12 items-center">
			<div>
				<h2 class="text-2xl font-semibold mb-4">What is Image Metadata?</h2>
				<p class="leading-relaxed">
					Metadata is like a digital fingerprint embedded in your images. It includes camera settings, location data, timestamps, and other technical details that can reveal sensitive information about your work, equipment, and even your location.
				</p>
			</div>
			<img src='/blog_imgs/metadata.png' alt="Metadata Example" class="rounded-lg shadow-md w-full" />
		</section>

		<!-- Types of Metadata -->
		<section>
			<h2 class="text-2xl font-semibold mb-8 text-center">Types of Metadata We Protect</h2>
			<div class="grid md:grid-cols-3 gap-8">
				<div class="border rounded-lg p-6 shadow-sm">
					<FileText class="h-6 w-6 text-primary mb-3" />
					<h3 class="text-lg font-semibold mb-2">EXIF Data</h3>
					<p>Camera settings, timestamps, and technical information that could reveal your equipment and shooting habits.</p>
					<img src="/blog_imgs/exif.png" class="mt-4 rounded-md" />
				</div>
				<div class="border rounded-lg p-6 shadow-sm">
					<Eye class="h-6 w-6 text-primary mb-3" />
					<h3 class="text-lg font-semibold mb-2">Location Data</h3>
					<p>GPS coordinates and location information that could compromise your privacy or reveal shooting locations.</p>
					<img src="/blog_imgs/gps.png" class="mt-4 rounded-md" />
				</div>
				<div class="border rounded-lg p-6 shadow-sm">
					<Settings class="h-6 w-6 text-primary mb-3" />
					<h3 class="text-lg font-semibold mb-2">Custom Metadata</h3>
					<p>User-added information like copyright notices, descriptions, and other custom fields.</p>
					<img src="/blog_imgs/custom_meta.png" class="mt-4 rounded-md" />
				</div>
			</div>
		</section>

		<!-- How It Works -->
		<section class="grid md:grid-cols-2 gap-12 items-center">
			<div>
				<h2 class="text-2xl font-semibold mb-4">How Our Protection Works</h2>
				<ol class="list-decimal space-y-4 pl-5">
					<li>
						<strong>Scan & Analyze:</strong> Our system automatically detects all metadata in your images.
					</li>
					<li>
						<strong>Select & Configure:</strong> Choose what information to keep, modify, or remove.
					</li>
					<li>
						<strong>Apply Protection:</strong> Process your images with the selected metadata settings.
					</li>
				</ol>
			</div>
			<img src="/blog_imgs/metadata_process.png" alt="Metadata Protection Process" class="rounded-lg shadow" />
		</section>

		<!-- Best Practices -->
		<section>
			<h2 class="text-2xl font-semibold mb-6">Best Practices for Metadata Protection</h2>
			<ul class="list-disc pl-6 space-y-2">
				<li>Always review metadata before sharing images on public platforms.</li>
				<li>Keep copyright and attribution information while removing sensitive data.</li>
				<li>Use different protection levels for different sharing scenarios.</li>
				<li>Maintain a backup of original images with full metadata for your records.</li>
			</ul>
		</section>

		<!-- Use Cases -->
		<section>
			<h2 class="text-2xl font-semibold mb-6 text-center">Common Use Cases</h2>
			<div class="grid sm:grid-cols-2 md:grid-cols-3 gap-6 text-center">
				<div class="p-4 border rounded-lg">
					<h3 class="font-semibold text-lg">Professional Photography</h3>
					<p class="text-sm text-gray-600 mt-2">Protect your shooting locations and equipment details from competitors.</p>
				</div>
				<div class="p-4 border rounded-lg">
					<h3 class="font-semibold text-lg">Social Media Sharing</h3>
					<p class="text-sm text-gray-600 mt-2">Remove sensitive metadata before posting images online.</p>
				</div>
				<div class="p-4 border rounded-lg">
					<h3 class="font-semibold text-lg">Client Deliverables</h3>
					<p class="text-sm text-gray-600 mt-2">Share images with appropriate metadata for client use.</p>
				</div>
			</div>
		</section>

		<!-- Behind The Scenes -->
		<section>
			<h2 class="text-2xl font-semibold mb-4">Technology Behind the Feature</h2>
			<p class="leading-relaxed">
				Our metadata protection uses advanced algorithms to analyze and modify image metadata while preserving image quality. We use industry-standard libraries like <code>ExifTool</code> and <code>Pillow</code> to ensure reliable metadata handling.
			</p>
			<p class="mt-4">
				The process is completely secure and happens in real-time. Your original images are never stored on our servers unless you explicitly choose to save them.
			</p>
		</section>
	</article>
</div> 