<script lang="ts">
	import { Button } from '$lib/components/ui/button';
	import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '$lib/components/ui/card';
	import {
		Shield,
		Lock,
		Eye,
		Download,
		FileText,
		ShieldCheck,
		Fingerprint,
		Camera,
		Search,
		Bell,
		ArrowRight,
		ArrowLeft
	} from 'lucide-svelte';
	import { goto } from '$app/navigation';
</script>

<div class="min-h-screen bg-gradient-to-b from-background to-muted/20">
	<div class="container mx-auto px-4 py-12">
		<!-- Back Button -->
		<div class="mb-8">
			<Button variant="ghost" class="gap-2" on:click={() => goto('/')}>
				<ArrowLeft class="h-4 w-4" />
				Back to Home
			</Button>
		</div>

		<!-- Hero Section -->
		<div class="mb-16 text-center">
			<h1 class="mb-4 text-5xl font-bold tracking-tight">Welcome to Authograph</h1>
			<p class="mx-auto max-w-2xl text-xl text-muted-foreground">
				Your comprehensive solution for protecting and managing digital images with advanced security features.
			</p>
		</div>

		<!-- Main Features Grid -->
		<div class="mb-16 grid gap-8 md:grid-cols-2 lg:grid-cols-3">
			<Card class="group relative overflow-hidden transition-all hover:shadow-lg">
				<CardHeader>
					<CardTitle class="flex items-center gap-2">
						<Fingerprint class="h-5 w-5" />
						Invisible Watermarking
					</CardTitle>
				</CardHeader>
				<CardContent>
					<CardDescription class="mb-4">
						Embed invisible watermarks in your images with customizable text and settings. Perfect for tracking image ownership and usage.
					</CardDescription>
					<a href="/learn/watermark" class="inline-flex items-center text-sm font-medium text-primary hover:underline">
						Learn more <ArrowRight class="ml-1 h-4 w-4" />
					</a>
				</CardContent>
			</Card>

			<Card class="group relative overflow-hidden transition-all hover:shadow-lg">
				<CardHeader>
					<CardTitle class="flex items-center gap-2">
						<Camera class="h-5 w-5" />
						AI Image Protection
					</CardTitle>
				</CardHeader>
				<CardContent>
					<CardDescription class="mb-4">
						Enable AI-powered protection for your images with customizable settings and real-time monitoring.
					</CardDescription>
					<a href="/learn/ai-protection" class="inline-flex items-center text-sm font-medium text-primary hover:underline">
						Learn more <ArrowRight class="ml-1 h-4 w-4" />
					</a>
				</CardContent>
			</Card>

			<Card class="group relative overflow-hidden transition-all hover:shadow-lg">
				<CardHeader>
					<CardTitle class="flex items-center gap-2">
						<Search class="h-5 w-5" />
						Image Metadata
					</CardTitle>
				</CardHeader>
				<CardContent>
					<CardDescription class="mb-4">
						Extract and manage image metadata, including EXIF data, camera information, and custom metadata fields.
					</CardDescription>
					<a href="/learn/metadata" class="inline-flex items-center text-sm font-medium text-primary hover:underline">
						Learn more <ArrowRight class="ml-1 h-4 w-4" />
					</a>
				</CardContent>
			</Card>

			<Card class="group relative overflow-hidden transition-all hover:shadow-lg">
				<CardHeader>
					<CardTitle class="flex items-center gap-2">
						<Lock class="h-5 w-5" />
						Access Control
					</CardTitle>
				</CardHeader>
				<CardContent>
					<CardDescription class="mb-4">
						Control image access with password protection, email restrictions, view limits, and OTP verification.
					</CardDescription>
					<a href="/learn/access" class="inline-flex items-center text-sm font-medium text-primary hover:underline">
						Learn more <ArrowRight class="ml-1 h-4 w-4" />
					</a>
				</CardContent>
			</Card>

			<Card class="group relative overflow-hidden transition-all hover:shadow-lg">
				<CardHeader>
					<CardTitle class="flex items-center gap-2">
						<Eye class="h-5 w-5" />
						Activity Monitoring
					</CardTitle>
				</CardHeader>
				<CardContent>
					<CardDescription class="mb-4">
						Track image access with detailed logs including IP addresses, locations, timestamps, and access types.
					</CardDescription>
					<a href="/learn/logs" class="inline-flex items-center text-sm font-medium text-primary hover:underline">
						Learn more <ArrowRight class="ml-1 h-4 w-4" />
					</a>
				</CardContent>
			</Card>

			<Card class="group relative overflow-hidden transition-all hover:shadow-lg">
				<CardHeader>
					<CardTitle class="flex items-center gap-2">
						<Bell class="h-5 w-5" />
						Smart Notifications
					</CardTitle>
				</CardHeader>
				<CardContent>
					<CardDescription class="mb-4">
						Receive real-time notifications for access requests, downloads, successful access, and failed attempts.
					</CardDescription>
					<a href="/learn/notifications" class="inline-flex items-center text-sm font-medium text-primary hover:underline">
						Learn more <ArrowRight class="ml-1 h-4 w-4" />
					</a>
				</CardContent>
			</Card>
		</div>

		<!-- Legal Links -->
		<div class="mb-16 grid gap-4 md:grid-cols-2">
			<Card class="group relative overflow-hidden transition-all hover:shadow-lg">
				<CardHeader>
					<CardTitle class="flex items-center gap-2">
						<FileText class="h-5 w-5" />
						Terms & Conditions
					</CardTitle>
				</CardHeader>
				<CardContent>
					<CardDescription class="mb-4">
						Read our terms of service and understand your rights and responsibilities.
					</CardDescription>
					<a href="/terms" class="inline-flex items-center text-sm font-medium text-primary hover:underline">
						Read Terms <ArrowRight class="ml-1 h-4 w-4" />
					</a>
				</CardContent>
			</Card>

			<Card class="group relative overflow-hidden transition-all hover:shadow-lg">
				<CardHeader>
					<CardTitle class="flex items-center gap-2">
						<ShieldCheck class="h-5 w-5" />
						Privacy Policy
					</CardTitle>
				</CardHeader>
				<CardContent>
					<CardDescription class="mb-4">
						Learn how we protect your privacy and handle your data.
					</CardDescription>
					<a href="/privacy" class="inline-flex items-center text-sm font-medium text-primary hover:underline">
						Read Policy <ArrowRight class="ml-1 h-4 w-4" />
					</a>
				</CardContent>
			</Card>
		</div>

		<!-- Call to Action -->
		<div class="rounded-lg border bg-card p-8 text-center shadow-lg">
			<h2 class="mb-4 text-3xl font-bold">Ready to Protect Your Images?</h2>
			<p class="mb-8 text-lg text-muted-foreground">
				Join thousands of users who trust Authograph to secure their digital assets.
			</p>
			<div class="flex justify-center gap-4">
				<Button size="lg" href="/register">Get Started Now</Button>
				<Button size="lg" variant="outline" href="/learn/watermark">Try Watermarking</Button>
			</div>
		</div>
	</div>
</div>
