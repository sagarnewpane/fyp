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

	<h1 class="mb-2 text-4xl font-bold">Terms & Conditions</h1>
	<p class="mb-8 text-sm text-muted-foreground">Last updated: March 15, 2024</p>

	<div class="prose prose-slate dark:prose-invert max-w-none">
		<section class="mb-8">
			<h2 class="text-2xl font-bold mb-4">1. Introduction</h2>
			<p>
				Welcome to Authograph. These Terms and Conditions govern your use of our website and services. By
				accessing or using Authograph, you agree to be bound by these Terms. If you disagree with any part of
				these terms, you may not access our services.
			</p>
		</section>

		<Separator class="my-8" />

		<section class="mb-8">
			<h2 class="text-2xl font-bold mb-4">2. Definitions</h2>
			<ul class="list-disc pl-6 space-y-2">
				<li>
					<strong>"Service"</strong> refers to the Authograph platform and all associated features and
					functionality.
				</li>
				<li>
					<strong>"User"</strong> refers to any individual or entity that accesses or uses the Service.
				</li>
				<li>
					<strong>"Content"</strong> refers to any images, text, or other materials uploaded to or
					processed through the Service.
				</li>
				<li>
					<strong>"Protected Content"</strong> refers to Content that has been secured using our
					protection features.
				</li>
			</ul>
		</section>

		<Separator class="my-8" />

		<section class="mb-8">
			<h2 class="text-2xl font-bold mb-4">3. Account Registration and Security</h2>
			<div class="space-y-4">
				<p>
					To use certain features of the Service, you must register for an account. You agree to:
				</p>
				<ul class="list-disc pl-6 space-y-2">
					<li>Provide accurate and complete information during registration</li>
					<li>Maintain the security of your account credentials</li>
					<li>Notify us immediately of any unauthorized access to your account</li>
					<li>Accept responsibility for all activities that occur under your account</li>
				</ul>
			</div>
		</section>

		<Separator class="my-8" />

		<section class="mb-8">
			<h2 class="text-2xl font-bold mb-4">4. User Content and Rights</h2>
			<div class="space-y-4">
				<p>
					By uploading Content to our Service, you:
				</p>
				<ul class="list-disc pl-6 space-y-2">
					<li>Retain all ownership rights to your Content</li>
					<li>Grant Authograph a license to process and protect your Content</li>
					<li>Ensure you have all necessary rights to upload and protect the Content</li>
					<li>Agree not to upload Content that violates any laws or third-party rights</li>
				</ul>
			</div>
		</section>

		<Separator class="my-8" />

		<section class="mb-8">
			<h2 class="text-2xl font-bold mb-4">5. Service Usage and Restrictions</h2>
			<div class="space-y-4">
				<p>You agree not to:</p>
				<ul class="list-disc pl-6 space-y-2">
					<li>Use the Service for any illegal purposes</li>
					<li>Attempt to bypass any security measures</li>
					<li>Interfere with the proper functioning of the Service</li>
					<li>Use automated systems or bots to access the Service</li>
					<li>Share access credentials with unauthorized parties</li>
				</ul>
			</div>
		</section>

		<Separator class="my-8" />

		<section class="mb-8">
			<h2 class="text-2xl font-bold mb-4">6. Intellectual Property</h2>
			<p>
				The Service and its original content, features, and functionality are owned by Authograph and are
				protected by international copyright, trademark, and other intellectual property laws. You may not
				copy, modify, or distribute any part of the Service without our explicit permission.
			</p>
		</section>

		<Separator class="my-8" />

		<section class="mb-8">
			<h2 class="text-2xl font-bold mb-4">7. Limitation of Liability</h2>
			<p>
				Authograph shall not be liable for any indirect, incidental, special, consequential, or punitive
				damages resulting from your use of or inability to use the Service. Our total liability for any
				claims related to the Service shall not exceed the amount paid by you, if any, for using the Service
				during the past 12 months.
			</p>
		</section>

		<Separator class="my-8" />

		<section class="mb-8">
			<h2 class="text-2xl font-bold mb-4">8. Termination</h2>
			<p>
				We may terminate or suspend your account and access to the Service immediately, without prior notice
				or liability, for any reason, including if you breach these Terms. Upon termination, your right to
				use the Service will immediately cease.
			</p>
		</section>

		<Separator class="my-8" />

		<section class="mb-8">
			<h2 class="text-2xl font-bold mb-4">9. Changes to Terms</h2>
			<p>
				We reserve the right to modify these Terms at any time. We will notify users of any material changes
				by posting the new Terms on this page and updating the "Last updated" date. Your continued use of
				the Service after such modifications constitutes your acceptance of the new Terms.
			</p>
		</section>

		<Separator class="my-8" />

		<section class="mb-8">
			<h2 class="text-2xl font-bold mb-4">10. Contact Information</h2>
			<p>
				If you have any questions about these Terms, please contact us at:
			</p>
			<Card class="mt-4">
				<CardHeader>
					<CardTitle>Contact Details</CardTitle>
				</CardHeader>
				<CardContent>
					<p>Email: support@authograph.com</p>
					<p>Address: Kathmandu, Nepal</p>
				</CardContent>
			</Card>
		</section>
	</div>

	<div class="mt-12 text-center">
		<Button variant="outline" href="/privacy">View Privacy Policy</Button>
	</div>
</div>
