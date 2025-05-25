<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Separator } from '$lib/components/ui/separator';
	import { ArrowLeft } from 'lucide-svelte';
	import { goto } from '$app/navigation';
</script>

<div class="container mx-auto max-w-4xl px-4 py-12">
	<!-- Back Button -->
	<div class="mb-8">
		<Button variant="ghost" class="gap-2" on:click={() => goto('/')}>
			<ArrowLeft class="h-4 w-4" />
			Back to Home
		</Button>
	</div>

	<h1 class="mb-2 text-4xl font-bold">Privacy Policy</h1>
	<p class="mb-8 text-sm text-muted-foreground">Last updated: March 15, 2024</p>

	<div class="prose prose-slate dark:prose-invert max-w-none">
		<section class="mb-8">
			<h2 class="text-2xl font-bold mb-4">1. Introduction</h2>
			<p>
				At Authograph, we take your privacy seriously. This Privacy Policy explains how we collect, use,
				disclose, and safeguard your information when you use our service. Please read this privacy policy
				carefully. If you do not agree with the terms of this privacy policy, please do not access the
				service.
			</p>
		</section>

		<Separator class="my-8" />

		<section class="mb-8">
			<h2 class="text-2xl font-bold mb-4">2. Information We Collect</h2>
			<div class="space-y-4">
				<h3 class="text-xl font-semibold">2.1 Personal Information</h3>
				<p>We may collect personal information that you voluntarily provide to us when you:</p>
				<ul class="list-disc pl-6 space-y-2">
					<li>Register for an account</li>
					<li>Upload images or content</li>
					<li>Set up access controls</li>
					<li>Contact our support team</li>
				</ul>

				<h3 class="text-xl font-semibold mt-6">2.2 Information Collected Automatically</h3>
				<p>When you use our service, we automatically collect:</p>
				<ul class="list-disc pl-6 space-y-2">
					<li>Device information (IP address, browser type, operating system)</li>
					<li>Usage data (pages visited, time spent, features used)</li>
					<li>Access logs and security-related information</li>
				</ul>
			</div>
		</section>

		<Separator class="my-8" />

		<section class="mb-8">
			<h2 class="text-2xl font-bold mb-4">3. How We Use Your Information</h2>
			<div class="space-y-4">
				<p>We use the information we collect to:</p>
				<ul class="list-disc pl-6 space-y-2">
					<li>Provide and maintain our service</li>
					<li>Process and protect your images</li>
					<li>Monitor and prevent unauthorized access</li>
					<li>Improve our service and user experience</li>
					<li>Communicate with you about your account</li>
					<li>Send security alerts and notifications</li>
				</ul>
			</div>
		</section>

		<Separator class="my-8" />

		<section class="mb-8">
			<h2 class="text-2xl font-bold mb-4">4. Data Security</h2>
			<p>
				We implement appropriate technical and organizational security measures to protect your personal
				information and content. This includes:
			</p>
			<ul class="list-disc pl-6 space-y-2 mt-4">
				<li>Encryption of data in transit and at rest</li>
				<li>Regular security assessments and updates</li>
				<li>Access controls and authentication measures</li>
				<li>Secure data storage and backup procedures</li>
			</ul>
		</section>

		<Separator class="my-8" />

		<section class="mb-8">
			<h2 class="text-2xl font-bold mb-4">5. Data Retention</h2>
			<p>
				We retain your personal information and content for as long as necessary to provide our services and
				comply with legal obligations. You can request deletion of your account and associated data at any
				time through your account settings.
			</p>
		</section>

		<Separator class="my-8" />

		<section class="mb-8">
			<h2 class="text-2xl font-bold mb-4">6. Your Rights</h2>
			<div class="space-y-4">
				<p>You have the right to:</p>
				<ul class="list-disc pl-6 space-y-2">
					<li>Access your personal information</li>
					<li>Correct inaccurate data</li>
					<li>Request deletion of your data</li>
					<li>Object to processing of your data</li>
					<li>Export your data</li>
					<li>Withdraw consent at any time</li>
				</ul>
			</div>
		</section>

		<Separator class="my-8" />

		<section class="mb-8">
			<h2 class="text-2xl font-bold mb-4">7. Cookies and Tracking</h2>
			<p>
				We use cookies and similar tracking technologies to improve your experience on our service. You can
				control cookie preferences through your browser settings. Essential cookies are required for the
				service to function properly.
			</p>
		</section>

		<Separator class="my-8" />

		<section class="mb-8">
			<h2 class="text-2xl font-bold mb-4">8. Third-Party Services</h2>
			<p>
				We may use third-party services to help us provide and improve our service. These services have
				their own privacy policies and may collect information as specified in their respective privacy
				policies.
			</p>
		</section>

		<Separator class="my-8" />

		<section class="mb-8">
			<h2 class="text-2xl font-bold mb-4">9. Children's Privacy</h2>
			<p>
				Our service is not intended for use by children under the age of 13. We do not knowingly collect
				personal information from children under 13. If you are a parent or guardian and believe your child
				has provided us with personal information, please contact us.
			</p>
		</section>

		<Separator class="my-8" />

		<section class="mb-8">
			<h2 class="text-2xl font-bold mb-4">10. Changes to This Policy</h2>
			<p>
				We may update this privacy policy from time to time. We will notify you of any changes by posting
				the new privacy policy on this page and updating the "Last updated" date. You are advised to review
				this privacy policy periodically for any changes.
			</p>
		</section>

		<Separator class="my-8" />

		<section class="mb-8">
			<h2 class="text-2xl font-bold mb-4">11. Contact Us</h2>
			<p>
				If you have any questions about this Privacy Policy, please contact us at:
			</p>
			<Card class="mt-4">
				<CardHeader>
					<CardTitle>Contact Details</CardTitle>
				</CardHeader>
				<CardContent>
					<p>Email: privacy@authograph.com</p>
					<p>Address: Kathmandu, Nepal</p>
				</CardContent>
			</Card>
		</section>
	</div>

	<div class="mt-12 text-center">
		<Button variant="outline" href="/terms">View Terms and Conditions</Button>
	</div>
</div>
