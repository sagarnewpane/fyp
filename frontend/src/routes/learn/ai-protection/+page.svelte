<script>
	import { Brain, Shield, Lock, Settings } from 'lucide-svelte';
</script>

<div class="w-full bg-white text-gray-800 py-16 px-6 lg:px-24">
	<article class="max-w-screen-xl mx-auto space-y-16">
		<!-- Hero Header -->
		<header class="text-center">
			<div class="flex justify-center mb-4">
				<Brain class="h-10 w-10 text-primary" />
			</div>
			<h1 class="text-4xl sm:text-5xl font-extrabold mb-4">AI Protection: The Future of Image Security</h1>
			<p class="text-xl text-gray-600 max-w-2xl mx-auto">
				Harness the power of artificial intelligence to protect your images from unauthorized use and manipulation. Our advanced AI system watches over your work 24/7.
			</p>
		</header>

		<!-- Intro Section -->
		<section class="grid md:grid-cols-2 gap-12 items-center">
			<div>
				<h2 class="text-2xl font-semibold mb-4">What is AI Protection?</h2>
				<p class="leading-relaxed">
					AI Protection is a cutting-edge security system that uses machine learning to monitor and protect your images. It can detect unauthorized use, identify manipulations, and track your images across the internet, all while learning and improving over time.
				</p>
			</div>
			<img src='/blog_imgs/ai_protection.png' alt="AI Protection Visualization" class="rounded-lg shadow-md w-full" />
		</section>

		<!-- Key Features -->
		<section>
			<h2 class="text-2xl font-semibold mb-8 text-center">Advanced Protection Features</h2>
			<div class="grid md:grid-cols-3 gap-8">
				<div class="border rounded-lg p-6 shadow-sm">
					<Brain class="h-6 w-6 text-primary mb-3" />
					<h3 class="text-lg font-semibold mb-2">Image Recognition</h3>
					<p>Our AI can identify your images even when they've been cropped, resized, or slightly modified.</p>
					<img src="/blog_imgs/ai_recognition.png" class="mt-4 rounded-md" />
				</div>
				<div class="border rounded-lg p-6 shadow-sm">
					<Shield class="h-6 w-6 text-primary mb-3" />
					<h3 class="text-lg font-semibold mb-2">Manipulation Detection</h3>
					<p>Detect when your images have been altered, edited, or used in unauthorized ways.</p>
					<img src="/blog_imgs/manipulation.png" class="mt-4 rounded-md" />
				</div>
				<div class="border rounded-lg p-6 shadow-sm">
					<Settings class="h-6 w-6 text-primary mb-3" />
					<h3 class="text-lg font-semibold mb-2">Smart Alerts</h3>
					<p>Get intelligent notifications about potential misuse, with context and suggested actions.</p>
					<img src="/blog_imgs/ai_alerts.png" class="mt-4 rounded-md" />
				</div>
			</div>
		</section>

		<!-- How It Works -->
		<section class="grid md:grid-cols-2 gap-12 items-center">
			<div>
				<h2 class="text-2xl font-semibold mb-4">How Our AI Protection Works</h2>
				<ol class="list-decimal space-y-4 pl-5">
					<li>
						<strong>Digital Fingerprinting:</strong> Our AI creates a unique signature for each protected image.
					</li>
					<li>
						<strong>Continuous Monitoring:</strong> The system scans the web 24/7 for matches to your images.
					</li>
					<li>
						<strong>Smart Analysis:</strong> Advanced algorithms analyze potential matches and detect manipulations.
					</li>
				</ol>
			</div>
			<img src="/blog_imgs/ai_process.png" alt="AI Protection Process" class="rounded-lg shadow" />
		</section>

		<!-- Best Practices -->
		<section>
			<h2 class="text-2xl font-semibold mb-6">Best Practices for AI Protection</h2>
			<ul class="list-disc pl-6 space-y-2">
				<li>Enable AI protection for all important images in your portfolio.</li>
				<li>Regularly review detection reports and adjust settings as needed.</li>
				<li>Combine AI protection with other security measures for maximum effectiveness.</li>
				<li>Keep your protection settings updated to benefit from the latest AI improvements.</li>
			</ul>
		</section>

		<!-- Use Cases -->
		<section>
			<h2 class="text-2xl font-semibold mb-6 text-center">Where AI Protection Excels</h2>
			<div class="grid sm:grid-cols-2 md:grid-cols-3 gap-6 text-center">
				<div class="p-4 border rounded-lg">
					<h3 class="font-semibold text-lg">Stock Photography</h3>
					<p class="text-sm text-gray-600 mt-2">Monitor and protect your entire stock image portfolio automatically.</p>
				</div>
				<div class="p-4 border rounded-lg">
					<h3 class="font-semibold text-lg">Brand Assets</h3>
					<p class="text-sm text-gray-600 mt-2">Protect company logos and branded imagery from unauthorized use.</p>
				</div>
				<div class="p-4 border rounded-lg">
					<h3 class="font-semibold text-lg">Artistic Works</h3>
					<p class="text-sm text-gray-600 mt-2">Safeguard your digital artwork and photography from theft.</p>
				</div>
			</div>
		</section>

		<!-- Behind The Scenes -->
		<section>
			<h2 class="text-2xl font-semibold mb-4">The Technology Behind AI Protection</h2>
			<p class="leading-relaxed">
				Our AI protection system uses state-of-the-art deep learning models, including convolutional neural networks (CNNs) and computer vision algorithms. We continuously train our models on new data to improve accuracy and stay ahead of new threats.
			</p>
			<p class="mt-4">
				The system is built on a scalable cloud infrastructure that can process millions of images daily, ensuring comprehensive protection without compromising performance.
			</p>
		</section>
	</article>
</div> 