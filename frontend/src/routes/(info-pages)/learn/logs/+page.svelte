<script>
	import { Eye, Clock, AlertTriangle, User, Download, Search } from 'lucide-svelte';
</script>

<div class="w-full bg-white px-6 py-16 text-gray-800 lg:px-24">
	<article class="mx-auto max-w-screen-xl space-y-16">
		<!-- Hero Header -->
		<header class="text-center">
			<div class="mb-4 flex justify-center">
				<Eye class="h-10 w-10 text-primary" />
			</div>
			<h1 class="mb-4 text-4xl font-extrabold sm:text-5xl">
				Activity Monitoring: Track Every Access
			</h1>
			<p class="mx-auto max-w-2xl text-xl text-gray-600">
				Monitor who's viewing your images, when they're being accessed, and from where. Get detailed
				insights into your content's usage and security.
			</p>
		</header>

		<!-- Intro Section -->
		<section class="grid items-center gap-12 md:grid-cols-2">
			<div>
				<h2 class="mb-4 text-2xl font-semibold">What is Activity Monitoring?</h2>
				<p class="leading-relaxed">
					Activity Monitoring provides real-time tracking of all interactions with your protected
					images. From views to downloads, every action is logged with detailed information about
					the user, time, location, and device used.
				</p>
			</div>
			<img
				src="/blog_imgs/logs.png"
				alt="Activity Monitoring Dashboard"
				class="w-full rounded-lg shadow-md"
			/>
		</section>

		<!-- Features -->
		<section>
			<h2 class="mb-8 text-center text-2xl font-semibold">Key Features</h2>
			<div class="grid gap-8 md:grid-cols-3">
				<div class="rounded-lg border p-6 shadow-sm">
					<Clock class="mb-3 h-6 w-6 text-primary" />
					<h3 class="mb-2 text-lg font-semibold">Real-time Tracking</h3>
					<p>
						Monitor access attempts as they happen with detailed timestamps and session information.
					</p>
				</div>
				<div class="rounded-lg border p-6 shadow-sm">
					<User class="mb-3 h-6 w-6 text-primary" />
					<h3 class="mb-2 text-lg font-semibold">User Analytics</h3>
					<p>Track who's accessing your images, their roles, and access patterns over time.</p>
				</div>
				<div class="rounded-lg border p-6 shadow-sm">
					<AlertTriangle class="mb-3 h-6 w-6 text-primary" />
					<h3 class="mb-2 text-lg font-semibold">Security Alerts</h3>
					<p>Get notified of suspicious activities or unauthorized access attempts.</p>
				</div>
			</div>
		</section>

		<!-- How It Works -->
		<section class="grid items-center gap-12 md:grid-cols-2">
			<div>
				<h2 class="mb-4 text-2xl font-semibold">How It Works</h2>
				<ol class="list-decimal space-y-4 pl-5">
					<li>
						<strong>Access Tracking:</strong> Every view, download, or share is automatically logged.
					</li>
					<li>
						<strong>Data Collection:</strong> We record IP addresses, timestamps, user agents, and access
						methods.
					</li>
					<li>
						<strong>Analysis:</strong> The system processes this data to provide meaningful insights.
					</li>
					<li>
						<strong>Reporting:</strong> View detailed reports and analytics in your dashboard.
					</li>
				</ol>
			</div>
			<img src="/blog_imgs/logs2.png" alt="Activity Logs Interface" class="rounded-lg shadow" />
		</section>

		<!-- Use Cases -->
		<section>
			<h2 class="mb-6 text-center text-2xl font-semibold">Common Use Cases</h2>
			<div class="grid gap-6 text-center sm:grid-cols-2 md:grid-cols-3">
				<div class="rounded-lg border p-4">
					<h3 class="text-lg font-semibold">Content Security</h3>
					<p class="mt-2 text-sm text-gray-600">
						Monitor who's accessing your sensitive images and when.
					</p>
				</div>
				<div class="rounded-lg border p-4">
					<h3 class="text-lg font-semibold">Usage Analytics</h3>
					<p class="mt-2 text-sm text-gray-600">
						Track how your images are being used and by whom.
					</p>
				</div>
				<div class="rounded-lg border p-4">
					<h3 class="text-lg font-semibold">Compliance</h3>
					<p class="mt-2 text-sm text-gray-600">
						Maintain audit trails for regulatory requirements.
					</p>
				</div>
			</div>
		</section>

		<!-- Behind The Scenes -->
		<section>
			<h2 class="mb-4 text-2xl font-semibold">Technology Behind the Feature</h2>
			<p class="leading-relaxed">
				Our activity monitoring system uses a combination of server-side logging and client-side
				tracking to capture comprehensive access data. The system:
			</p>
			<ul class="mt-4 list-disc space-y-2 pl-6">
				<li>Logs all API requests and responses</li>
				<li>Tracks user sessions and authentication events</li>
				<li>Monitors file access and download patterns</li>
				<li>Analyzes access patterns for suspicious behavior</li>
			</ul>
			<p class="mt-4">
				All logs are stored securely and can be exported for analysis or compliance purposes. The
				system uses efficient database indexing to ensure quick access to historical data.
			</p>
		</section>
	</article>
</div>
