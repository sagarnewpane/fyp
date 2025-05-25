<script>
	import { FileText, Lock, Eye, Settings } from 'lucide-svelte';
</script>

<div class="w-full bg-white px-6 py-16 text-gray-800 lg:px-24">
	<article class="mx-auto max-w-screen-xl space-y-16">
		<!-- Hero Header -->
		<header class="text-center">
			<div class="mb-4 flex justify-center">
				<FileText class="h-10 w-10 text-primary" />
			</div>
			<h1 class="mb-4 text-4xl font-extrabold sm:text-5xl">
				Metadata Protection: Guard Your Digital Footprint
			</h1>
			<p class="mx-auto max-w-2xl text-xl text-gray-600">
				Every image carries hidden information that could reveal more than you intend. Learn how to
				control what metadata stays with your images and what gets removed.
			</p>
		</header>

		<!-- Intro Section -->
		<section class="grid items-center gap-12 md:grid-cols-2">
			<div>
				<h2 class="mb-4 text-2xl font-semibold">What is Image Metadata?</h2>
				<p class="leading-relaxed">
					Metadata is like a digital fingerprint embedded in your images. It includes camera
					settings, location data, timestamps, and other technical details that can reveal sensitive
					information about your work, equipment, and even your location.
				</p>
			</div>
			<img
				src="/blog_imgs/metadata.png"
				alt="Metadata Example"
				class="w-full rounded-lg shadow-md"
			/>
		</section>

		<!-- Types of Metadata -->
		<section>
			<h2 class="mb-8 text-center text-2xl font-semibold">Types of Metadata We Protect</h2>
			<div class="grid gap-8 md:grid-cols-3">
				<div class="rounded-lg border p-6 shadow-sm">
					<FileText class="mb-3 h-6 w-6 text-primary" />
					<h3 class="mb-2 text-lg font-semibold">EXIF Data</h3>
					<p>
						Camera settings, timestamps, and technical information that could reveal your equipment
						and shooting habits.
					</p>
				</div>
				<div class="rounded-lg border p-6 shadow-sm">
					<Eye class="mb-3 h-6 w-6 text-primary" />
					<h3 class="mb-2 text-lg font-semibold">Location Data</h3>
					<p>
						GPS coordinates and location information that could compromise your privacy or reveal
						shooting locations.
					</p>
				</div>
				<div class="rounded-lg border p-6 shadow-sm">
					<Settings class="mb-3 h-6 w-6 text-primary" />
					<h3 class="mb-2 text-lg font-semibold">Custom Metadata</h3>
					<p>
						User-added information like copyright notices, descriptions, and other custom fields.
					</p>
				</div>
			</div>
		</section>

		<!-- How It Works -->
		<section class="grid items-center gap-12 md:grid-cols-2">
			<div>
				<h2 class="mb-4 text-2xl font-semibold">How Our Protection Works</h2>
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
			<img
				src="/blog_imgs/metadata.png"
				alt="Metadata Protection Process"
				class="rounded-lg shadow"
			/>
		</section>

		<!-- Best Practices -->
		<section>
			<h2 class="mb-6 text-2xl font-semibold">Best Practices for Metadata Protection</h2>
			<ul class="list-disc space-y-2 pl-6">
				<li>Always review metadata before sharing images on public platforms.</li>
				<li>Keep copyright and attribution information while removing sensitive data.</li>
				<li>Use different protection levels for different sharing scenarios.</li>
				<li>Maintain a backup of original images with full metadata for your records.</li>
			</ul>
		</section>

		<!-- Use Cases -->
		<section>
			<h2 class="mb-6 text-center text-2xl font-semibold">Common Use Cases</h2>
			<div class="grid gap-6 text-center sm:grid-cols-2 md:grid-cols-3">
				<div class="rounded-lg border p-4">
					<h3 class="text-lg font-semibold">Professional Photography</h3>
					<p class="mt-2 text-sm text-gray-600">
						Protect your shooting locations and equipment details from competitors.
					</p>
				</div>
				<div class="rounded-lg border p-4">
					<h3 class="text-lg font-semibold">Social Media Sharing</h3>
					<p class="mt-2 text-sm text-gray-600">
						Remove sensitive metadata before posting images online.
					</p>
				</div>
				<div class="rounded-lg border p-4">
					<h3 class="text-lg font-semibold">Client Deliverables</h3>
					<p class="mt-2 text-sm text-gray-600">
						Share images with appropriate metadata for client use.
					</p>
				</div>
			</div>
		</section>

		<!-- Behind The Scenes -->
		<section>
			<h2 class="mb-4 text-2xl font-semibold">Technology Behind the Feature</h2>
			<p class="leading-relaxed">
				Our metadata protection uses advanced algorithms to analyze and modify image metadata while
				preserving image quality. We use industry-standard libraries like <code>ExifTool</code> and
				<code>Pillow</code> to ensure reliable metadata handling.
			</p>
			<p class="mt-4">
				The process is completely secure and happens in real-time. Your original images are never
				stored on our servers unless you explicitly choose to save them.
			</p>
		</section>
	</article>
</div>
