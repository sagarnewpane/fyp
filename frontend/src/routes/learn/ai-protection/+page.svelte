<script>
	import { Brain, Shield, Lock, Settings } from 'lucide-svelte';
</script>

<div class="container mx-auto max-w-4xl px-4 py-8">
	<header class="mb-8">
		<div class="mb-4 flex items-center gap-3">
			<Brain class="h-8 w-8 text-primary" />
			<h1 class="text-3xl font-bold">AI Protection</h1>
		</div>
		<p class="text-xl text-muted-foreground">
			Learn how artificial intelligence can help protect your images from unauthorized use and manipulation.
		</p>
	</header>

	<article class="prose prose-lg max-w-none">
		<section class="mb-8">
			<h2>What is AI Protection?</h2>
			<p>
				AI Protection uses advanced machine learning algorithms to detect and prevent unauthorized use of your
				images. It can identify when your images are being used without permission and help track their
				distribution across the internet.
			</p>
		</section>

		<section class="mb-8">
			<h2>Key Features</h2>
			<div class="grid gap-6 md:grid-cols-2">
				<div class="rounded-lg border p-4">
					<Brain class="mb-2 h-6 w-6 text-primary" />
					<h3 class="text-xl font-semibold">Image Recognition</h3>
					<p>AI-powered detection of your images across the web.</p>
				</div>
				<div class="rounded-lg border p-4">
					<Shield class="mb-2 h-6 w-6 text-primary" />
					<h3 class="text-xl font-semibold">Manipulation Detection</h3>
					<p>Identify when your images have been altered or edited.</p>
				</div>
				<div class="rounded-lg border p-4">
					<Settings class="mb-2 h-6 w-6 text-primary" />
					<h3 class="text-xl font-semibold">Customizable Alerts</h3>
					<p>Set up notifications for unauthorized use of your images.</p>
				</div>
			</div>
		</section>

		<section class="mb-8">
			<h2>How It Works</h2>
			<ol class="list-decimal pl-6">
				<li class="mb-4">
					<strong>Image Analysis</strong>
					<p>AI algorithms analyze your images to create unique digital fingerprints.</p>
				</li>
				<li class="mb-4">
					<strong>Continuous Monitoring</strong>
					<p>Regular scanning of the web for matches to your protected images.</p>
				</li>
				<li class="mb-4">
					<strong>Alert System</strong>
					<p>Receive notifications when your images are detected in unauthorized use.</p>
				</li>
			</ol>
		</section>

		<section class="mb-8">
			<h2>Best Practices</h2>
			<ul class="list-disc pl-6">
				<li>Enable AI protection for all important images</li>
				<li>Regularly review detection reports and alerts</li>
				<li>Combine AI protection with other security measures</li>
				<li>Keep your protection settings up to date</li>
			</ul>
		</section>

		<section class="mb-8">
			<h2>Common Use Cases</h2>
			<div class="grid gap-4">
				<div class="rounded-lg border p-4">
					<h3 class="text-xl font-semibold">Stock Photography</h3>
					<p>Monitor and protect your stock image portfolio.</p>
				</div>
				<div class="rounded-lg border p-4">
					<h3 class="text-xl font-semibold">Brand Assets</h3>
					<p>Protect company logos and branded imagery.</p>
				</div>
				<div class="rounded-lg border p-4">
					<h3 class="text-xl font-semibold">Artistic Works</h3>
					<p>Safeguard your digital artwork and photography.</p>
				</div>
			</div>
		</section>
	</article>
</div> 