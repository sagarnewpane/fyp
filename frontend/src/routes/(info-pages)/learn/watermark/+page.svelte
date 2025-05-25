<script>
	import { Fingerprint, Image, Shield } from 'lucide-svelte';
</script>

<div class="w-full bg-white px-6 py-16 text-gray-800 lg:px-24">
	<article class="mx-auto max-w-screen-xl space-y-16">
		<!-- Hero Header -->
		<header class="text-center">
			<div class="mb-4 flex justify-center">
				<Fingerprint class="h-10 w-10 text-primary" />
			</div>
			<h1 class="mb-4 text-4xl font-extrabold sm:text-5xl">
				Image Watermarking: Protect What’s Yours
			</h1>
			<p class="mx-auto max-w-2xl text-xl text-gray-600">
				Watermarking lets you stamp your ownership on digital images — visibly or invisibly. In this
				guide, learn what it is, why it matters, and how to use it effectively.
			</p>
		</header>

		<!-- Intro Section -->
		<section class="grid items-center gap-12 md:grid-cols-2">
			<div>
				<h2 class="mb-4 text-2xl font-semibold">What is Image Watermarking?</h2>
				<p class="leading-relaxed">
					Watermarking is the process of embedding copyright information into your images. Whether
					it's a visible logo or a hidden identifier, watermarking gives you a way to claim your
					work and deter image theft — especially in an age where content is freely shared.
				</p>
			</div>
			<img
				src="/blog_imgs/watermark.png"
				alt="Watermarked Image Example"
				class=" rounded-lg shadow-md"
			/>
		</section>

		<!-- Types of Watermarks -->
		<section>
			<h2 class="mb-8 text-center text-2xl font-semibold">Types of Watermarks</h2>
			<div class="grid gap-8 md:grid-cols-3">
				<div class="rounded-lg border p-6 shadow-sm">
					<Image class="mb-3 h-6 w-6 text-primary" />
					<h3 class="mb-2 text-lg font-semibold">Visible Watermarks</h3>
					<p>
						Text or logo overlays placed directly over the image — often semi-transparent or in a
						corner.
					</p>
					<img src="/blog_imgs/watermark.webp" class="mt-4 rounded-md" />
				</div>
				<div class="rounded-lg border p-6 shadow-sm">
					<Shield class="mb-3 h-6 w-6 text-primary" />
					<h3 class="mb-2 text-lg font-semibold">Invisible Watermarks</h3>
					<p>
						Steganographic techniques hide data in image pixels — useful for legal proof or content
						tracking.
					</p>
					<img src="/blog_imgs/hidden.png" class="mt-4 rounded-md" />
				</div>
				<div class="rounded-lg border p-6 shadow-sm">
					<h3 class="mb-2 text-lg font-semibold">Customizable Options</h3>
					<p>
						Choose position, opacity, size, text content, and image overlay to match your brand
						identity.
					</p>
					<img src="/blog_imgs/watermark_settings.png" class="mt-4 rounded-md" />
				</div>
			</div>
		</section>

		<!-- How It Works -->
		<section class="grid items-center gap-12 md:grid-cols-2">
			<div>
				<h2 class="mb-4 text-2xl font-semibold">How It Works on Our Platform</h2>
				<ol class="list-decimal space-y-4 pl-5">
					<li>
						<strong>Select the watermark type:</strong> Visible, invisible, or both.
					</li>
					<li>
						<strong>Customize it:</strong> Type your signature in any way.
					</li>
					<li>
						<strong>Apply protection:</strong> The system embeds your watermark and secures the image.
					</li>
				</ol>
			</div>
			<img src="/blog_imgs/watermark2.png" class="rounded-lg shadow" />
		</section>

		<!-- Best Practices -->
		<section>
			<h2 class="mb-6 text-2xl font-semibold">Watermarking Best Practices</h2>
			<ul class="list-disc space-y-2 pl-6">
				<li>Use watermarks on previews or shared work to deter casual theft.</li>
				<li>Position them strategically — corner, center, or tiled, based on risk.</li>
				<li>Invisible watermarks are best for high-value content with traceability needs.</li>
				<li>Regularly update your watermark to keep ahead of removal tools.</li>
			</ul>
		</section>

		<!-- Use Cases -->
		<section>
			<h2 class="mb-6 text-center text-2xl font-semibold">Where It’s Used</h2>
			<div class="grid gap-6 text-center sm:grid-cols-2 md:grid-cols-3">
				<div class="rounded-lg border p-4">
					<h3 class="text-lg font-semibold">Photography Portfolios</h3>
					<p class="mt-2 text-sm text-gray-600">
						Protect your work while showcasing it to potential clients.
					</p>
				</div>
				<div class="rounded-lg border p-4">
					<h3 class="text-lg font-semibold">Stock Agencies</h3>
					<p class="mt-2 text-sm text-gray-600">
						Deliver watermarked previews to prevent unpaid use.
					</p>
				</div>
				<div class="rounded-lg border p-4">
					<h3 class="text-lg font-semibold">Digital Art Sharing</h3>
					<p class="mt-2 text-sm text-gray-600">
						Assert your authorship on platforms like DeviantArt or Behance.
					</p>
				</div>
			</div>
		</section>

		<!-- Behind The Scenes -->
		<section>
			<h2 class="mb-4 text-2xl font-semibold">Technology Behind the Feature</h2>
			<p class="leading-relaxed">
				We use techniques like <strong>DWT (Discrete Wavelet Transform)</strong> and embedding for invisible
				watermarking. These methods subtly alter the image data to store information that’s robust but
				hidden.
			</p>
			<p class="mt-4">
				All watermarking is done securely using Python libraries like <code>Pillow</code> and
				<code>OpenCV</code>. The process is efficient, and no images are stored permanently on the
				server unless you choose to.
			</p>
		</section>
	</article>
</div>
