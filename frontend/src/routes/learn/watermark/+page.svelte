<script>
	import { Fingerprint, Image, Shield } from 'lucide-svelte';
</script>

<div class="w-full bg-white text-gray-800 py-16 px-6 lg:px-24">
	<article class="max-w-screen-xl mx-auto space-y-16">
		<!-- Hero Header -->
		<header class="text-center">
			<div class="flex justify-center mb-4">
				<Fingerprint class="h-10 w-10 text-primary" />
			</div>
			<h1 class="text-4xl sm:text-5xl font-extrabold mb-4">Image Watermarking: Protect What’s Yours</h1>
			<p class="text-xl text-gray-600 max-w-2xl mx-auto">
				Watermarking lets you stamp your ownership on digital images — visibly or invisibly. In this guide, learn what it is, why it matters, and how to use it effectively.
			</p>
		</header>

		<!-- Intro Section -->
		<section class="grid md:grid-cols-2 gap-12 items-center">
			<div>
				<h2 class="text-2xl font-semibold mb-4">What is Image Watermarking?</h2>
				<p class="leading-relaxed">
					Watermarking is the process of embedding copyright information into your images. Whether it's a visible logo or a hidden identifier, watermarking gives you a way to claim your work and deter image theft — especially in an age where content is freely shared.
				</p>
			</div>
			<img src='/blog_imgs/watermark.png' alt="Watermarked Image Example" class="rounded-lg shadow-md w-full" />
		</section>

		<!-- Types of Watermarks -->
		<section>
			<h2 class="text-2xl font-semibold mb-8 text-center">Types of Watermarks</h2>
			<div class="grid md:grid-cols-3 gap-8">
				<div class="border rounded-lg p-6 shadow-sm">
					<Image class="h-6 w-6 text-primary mb-3" />
					<h3 class="text-lg font-semibold mb-2">Visible Watermarks</h3>
					<p>Text or logo overlays placed directly over the image — often semi-transparent or in a corner.</p>
					<img src="/blog_imgs/watermark.webp" class="mt-4 rounded-md" />
				</div>
				<div class="border rounded-lg p-6 shadow-sm">
					<Shield class="h-6 w-6 text-primary mb-3" />
					<h3 class="text-lg font-semibold mb-2">Invisible Watermarks</h3>
					<p>Steganographic techniques hide data in image pixels — useful for legal proof or content tracking.</p>
					<img src="/blog_imgs/hidden.png" class="mt-4 rounded-md" />
				</div>
				<div class="border rounded-lg p-6 shadow-sm">
					<h3 class="text-lg font-semibold mb-2">Customizable Options</h3>
					<p>Choose position, opacity, size, text content, and image overlay to match your brand identity.</p>
					<img src="/blog_imgs/watermark_settings.png" class="mt-4 rounded-md" />
				</div>
			</div>
		</section>

		<!-- How It Works -->
		<section class="grid md:grid-cols-2 gap-12 items-center">
			<div>
				<h2 class="text-2xl font-semibold mb-4">How It Works on Our Platform</h2>
				<ol class="list-decimal space-y-4 pl-5">
					<li>
						<strong>Select the watermark type:</strong> Visible, invisible, or both.
					</li>
					<li>
						<strong>Customize it:</strong> Upload your logo or type your signature.
					</li>
					<li>
						<strong>Apply protection:</strong> The system embeds your watermark and secures the image.
					</li>
				</ol>
			</div>
			<img src="https://via.placeholder.com/500x300?text=Watermarking+Process+Flow" class="rounded-lg shadow" />
		</section>

		<!-- Best Practices -->
		<section>
			<h2 class="text-2xl font-semibold mb-6">Watermarking Best Practices</h2>
			<ul class="list-disc pl-6 space-y-2">
				<li>Use watermarks on previews or shared work to deter casual theft.</li>
				<li>Position them strategically — corner, center, or tiled, based on risk.</li>
				<li>Invisible watermarks are best for high-value content with traceability needs.</li>
				<li>Regularly update your watermark to keep ahead of removal tools.</li>
			</ul>
		</section>

		<!-- Use Cases -->
		<section>
			<h2 class="text-2xl font-semibold mb-6 text-center">Where It’s Used</h2>
			<div class="grid sm:grid-cols-2 md:grid-cols-3 gap-6 text-center">
				<div class="p-4 border rounded-lg">
					<h3 class="font-semibold text-lg">Photography Portfolios</h3>
					<p class="text-sm text-gray-600 mt-2">Protect your work while showcasing it to potential clients.</p>
				</div>
				<div class="p-4 border rounded-lg">
					<h3 class="font-semibold text-lg">Stock Agencies</h3>
					<p class="text-sm text-gray-600 mt-2">Deliver watermarked previews to prevent unpaid use.</p>
				</div>
				<div class="p-4 border rounded-lg">
					<h3 class="font-semibold text-lg">Digital Art Sharing</h3>
					<p class="text-sm text-gray-600 mt-2">Assert your authorship on platforms like DeviantArt or Behance.</p>
				</div>
			</div>
		</section>

		<!-- Behind The Scenes -->
		<section>
			<h2 class="text-2xl font-semibold mb-4">Technology Behind the Feature</h2>
			<p class="leading-relaxed">
				We use techniques like <strong>DCT (Discrete Cosine Transform)</strong> and <strong>LSB (Least Significant Bit)</strong> embedding for invisible watermarking. These methods subtly alter the image data to store information that’s robust but hidden.
			</p>
			<p class="mt-4">
				All watermarking is done securely using Python libraries like <code>Pillow</code> and <code>OpenCV</code>. The process is efficient, and no images are stored permanently on the server unless you choose to.
			</p>
		</section>
	</article>
</div>
