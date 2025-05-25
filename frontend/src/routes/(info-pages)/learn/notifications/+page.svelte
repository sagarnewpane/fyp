<script>
	import { Bell, AlertCircle, Settings, Mail, Shield, Clock } from 'lucide-svelte';
</script>

<div class="w-full bg-white px-6 py-16 text-gray-800 lg:px-24">
	<article class="mx-auto max-w-screen-xl space-y-16">
		<!-- Hero Header -->
		<header class="text-center">
			<div class="mb-4 flex justify-center">
				<Bell class="h-10 w-10 text-primary" />
			</div>
			<h1 class="mb-4 text-4xl font-extrabold sm:text-5xl">Smart Notifications: Stay Informed</h1>
			<p class="mx-auto max-w-2xl text-xl text-gray-600">
				Get real-time alerts about your images' security status, access attempts, and important
				events. Stay in control with customizable notification settings.
			</p>
		</header>

		<!-- Intro Section -->
		<section class="grid items-center gap-12 md:grid-cols-2">
			<div>
				<h2 class="mb-4 text-2xl font-semibold">What are Smart Notifications?</h2>
				<p class="leading-relaxed">
					Smart Notifications keep you informed about all important events related to your protected
					images. From security alerts to access notifications, you'll never miss a critical update
					about your content.
				</p>
			</div>
			<img
				src="/blog_imgs/notifications.png"
				alt="Notifications Dashboard"
				class="w-full rounded-lg shadow-md"
			/>
		</section>

		<!-- Features -->
		<section>
			<h2 class="mb-8 text-center text-2xl font-semibold">Key Features</h2>
			<div class="grid gap-8 md:grid-cols-3">
				<div class="rounded-lg border p-6 shadow-sm">
					<AlertCircle class="mb-3 h-6 w-6 text-primary" />
					<h3 class="mb-2 text-lg font-semibold">Security Alerts</h3>
					<p>
						Get notified of suspicious activities, unauthorized access attempts, and potential
						security threats.
					</p>
				</div>
				<div class="rounded-lg border p-6 shadow-sm">
					<Clock class="mb-3 h-6 w-6 text-primary" />
					<h3 class="mb-2 text-lg font-semibold">Real-time Updates</h3>
					<p>Receive instant notifications about image views, downloads, and access changes.</p>
				</div>
				<div class="rounded-lg border p-6 shadow-sm">
					<Settings class="mb-3 h-6 w-6 text-primary" />
					<h3 class="mb-2 text-lg font-semibold">Customizable Settings</h3>
					<p>Choose which events trigger notifications and how you want to receive them.</p>
				</div>
			</div>
		</section>

		<!-- How It Works -->
		<section class="grid items-center gap-12 md:grid-cols-2">
			<div>
				<h2 class="mb-4 text-2xl font-semibold">How It Works</h2>
				<ol class="list-decimal space-y-4 pl-5">
					<li>
						<strong>Event Detection:</strong> The system monitors all activities related to your images.
					</li>
					<li>
						<strong>Notification Rules:</strong> Your preferences determine which events trigger alerts.
					</li>
					<li>
						<strong>Delivery:</strong> Notifications are sent through your preferred channels.
					</li>
					<li>
						<strong>Action:</strong> Respond to notifications directly from your dashboard or email.
					</li>
				</ol>
			</div>
		</section>

		<!-- Notification Types -->
		<section>
			<h2 class="mb-6 text-center text-2xl font-semibold">Types of Notifications</h2>
			<div class="grid gap-6 text-center sm:grid-cols-2 md:grid-cols-3">
				<div class="rounded-lg border p-4">
					<Shield class="mx-auto mb-2 h-6 w-6 text-primary" />
					<h3 class="text-lg font-semibold">Security Events</h3>
					<p class="mt-2 text-sm text-gray-600">
						Unauthorized access, suspicious activities, and security breaches.
					</p>
				</div>
				<div class="rounded-lg border p-4">
					<Mail class="mx-auto mb-2 h-6 w-6 text-primary" />
					<h3 class="text-lg font-semibold">Access Updates</h3>
					<p class="mt-2 text-sm text-gray-600">
						New access requests, permission changes, and download events.
					</p>
				</div>
				<div class="rounded-lg border p-4">
					<Settings class="mx-auto mb-2 h-6 w-6 text-primary" />
					<h3 class="text-lg font-semibold">System Updates</h3>
					<p class="mt-2 text-sm text-gray-600">
						Feature updates, maintenance notifications, and service status.
					</p>
				</div>
			</div>
		</section>

		<!-- Behind The Scenes -->
		<section>
			<h2 class="mb-4 text-2xl font-semibold">Technology Behind the Feature</h2>
			<p class="leading-relaxed">
				Our notification system uses a robust event-driven architecture to ensure reliable delivery
				of alerts. The system:
			</p>
			<p class="mt-4">
				All notifications are processed asynchronously to ensure system performance isn't affected.
				The system includes retry mechanisms and fallback options to guarantee delivery.
			</p>
		</section>
	</article>
</div>
