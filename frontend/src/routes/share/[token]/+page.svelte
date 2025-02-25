<script>
	import { onMount } from 'svelte';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import {
		Card,
		CardContent,
		CardHeader,
		CardTitle,
		CardDescription
	} from '$lib/components/ui/card';
	import { Alert, AlertDescription, AlertTitle } from '$lib/components/ui/alert';
	import { Label } from '$lib/components/ui/label';
	import { Lock, Download, Share2, X, Eye, Mail, Key, ArrowLeft } from 'lucide-svelte';
	import { toast } from 'svelte-sonner';
	import { slide } from 'svelte/transition';
	import { browser } from '$app/environment';

	export let data;

	let accessStep = 'email';
	let email = '';
	let password = '';
	let otp = '';
	let imageData = null;
	let showInfo = true;
	let isLoading = false;
	let accessFormError = '';

	// Form validation
	$: isValidEmail = email && email.includes('@') && email.includes('.');
	$: isValidPassword = password && password.length >= 1;
	$: isValidOTP = otp && otp.length >= 4;

	async function handleEmailSubmit() {
		if (!isValidEmail || !browser) return;

		isLoading = true;
		accessFormError = '';

		try {
			const response = await fetch(`/api/access/${data.token}/initiate/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ email })
			});

			const result = await response.json();

			if (response.status === 403) {
				throw new Error('Email not authorized to access this content');
			}

			if (result.requires_password) {
				accessStep = 'password';
				toast?.info('Password required for access');
			} else {
				accessStep = 'otp';
				toast?.success('Verification code sent to your email');
			}
		} catch (error) {
			console.error('Error:', error);
			accessFormError = error.message;
			toast?.error(error.message);
		} finally {
			isLoading = false;
		}
	}

	async function handlePasswordSubmit() {
		if (!isValidPassword || !browser) return;

		isLoading = true;
		accessFormError = '';

		try {
			const response = await fetch(`/api/access/${data.token}/initiate/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					email,
					password
				})
			});

			const result = await response.json();

			if (!response.ok) {
				throw new Error(result.error || 'Invalid password');
			}

			accessStep = 'otp';
			toast?.success('Verification code sent to your email');
		} catch (error) {
			accessFormError = error.message;
			toast?.error(error.message);
		} finally {
			isLoading = false;
		}
	}

	async function handleOTPSubmit() {
		if (!isValidOTP || !browser) return;

		isLoading = true;
		accessFormError = '';

		try {
			const response = await fetch(`/api/access/${data.token}/verify/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ email, otp })
			});

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.error || 'Invalid verification code');
			}

			const accessData = await response.json();
			imageData = accessData;
			accessStep = 'viewing';
		} catch (error) {
			accessFormError = error.message;
			toast?.error(error.message);
		} finally {
			isLoading = false;
		}
	}

	function handleDownload() {
		if (!browser) return;
		if (imageData?.allow_download) {
			const link = document.createElement('a');
			link.href = imageData.image_url;
			link.download = '';
			document.body.appendChild(link);
			link.click();
			document.body.removeChild(link);
			toast?.success('Downloading image...');
		}
	}

	function handleShare() {
		if (!browser) return;
		navigator.clipboard.writeText(window.location.href);
		toast?.success('Link copied to clipboard');
	}

	function toggleInfo() {
		showInfo = !showInfo;
	}

	function goBack() {
		if (accessStep === 'password') {
			accessStep = 'email';
		} else if (accessStep === 'otp') {
			accessStep = password ? 'password' : 'email';
		}
		accessFormError = '';
	}
</script>

<div class="min-h-screen bg-background">
	{#if accessStep !== 'viewing'}
		<div class="flex min-h-screen items-center justify-center p-4">
			<Card class="w-full max-w-md">
				<CardHeader class="text-center">
					<Lock class="mx-auto h-12 w-12 text-primary" />
					<CardTitle class="mt-4 text-2xl">Protected Content</CardTitle>
					<CardDescription>
						{#if accessStep === 'email'}
							Please enter your email to continue
						{:else if accessStep === 'password'}
							This content is password protected
						{:else if accessStep === 'otp'}
							Enter the verification code sent to your email
						{/if}
					</CardDescription>
				</CardHeader>

				<CardContent class="space-y-6">
					{#if accessFormError}
						<Alert variant="destructive">
							<AlertDescription>{accessFormError}</AlertDescription>
						</Alert>
					{/if}

					{#if accessStep === 'email'}
						<form class="space-y-4" on:submit|preventDefault={handleEmailSubmit}>
							<div class="space-y-2">
								<Label for="email">Email Address</Label>
								<div class="relative">
									<Mail class="absolute left-3 top-2.5 h-5 w-5 text-muted-foreground" />
									<Input
										id="email"
										type="email"
										placeholder="Enter your email"
										class="pl-10"
										bind:value={email}
										disabled={isLoading}
									/>
								</div>
							</div>

							<Button type="submit" class="w-full" disabled={!isValidEmail || isLoading}>
								{#if isLoading}
									<div class="mr-2 h-4 w-4 animate-spin rounded-full border-b-2 border-white" />
								{/if}
								Continue
							</Button>
						</form>
					{:else if accessStep === 'password'}
						<form class="space-y-4" on:submit|preventDefault={handlePasswordSubmit}>
							<div class="space-y-2">
								<Label for="password">Password</Label>
								<div class="relative">
									<Key class="absolute left-3 top-2.5 h-5 w-5 text-muted-foreground" />
									<Input
										id="password"
										type="password"
										placeholder="Enter access password"
										class="pl-10"
										bind:value={password}
										disabled={isLoading}
									/>
								</div>
							</div>

							<Button type="submit" class="w-full" disabled={!isValidPassword || isLoading}>
								{#if isLoading}
									<div class="mr-2 h-4 w-4 animate-spin rounded-full border-b-2 border-white" />
								{/if}
								Verify Password
							</Button>

							<Button variant="ghost" class="w-full" on:click={goBack} disabled={isLoading}>
								<ArrowLeft class="mr-2 h-4 w-4" />
								Back
							</Button>
						</form>
					{:else if accessStep === 'otp'}
						<form class="space-y-4" on:submit|preventDefault={handleOTPSubmit}>
							<div class="space-y-2">
								<Label for="otp">Verification Code</Label>
								<Input
									id="otp"
									type="text"
									placeholder="Enter verification code"
									class="text-center text-lg tracking-widest"
									bind:value={otp}
									disabled={isLoading}
									maxlength="6"
								/>
								<p class="text-sm text-muted-foreground">
									Enter the 6-digit code sent to {email}
								</p>
							</div>

							<Button type="submit" class="w-full" disabled={!isValidOTP || isLoading}>
								{#if isLoading}
									<div class="mr-2 h-4 w-4 animate-spin rounded-full border-b-2 border-white" />
								{/if}
								Verify Code
							</Button>

							<Button variant="ghost" class="w-full" on:click={goBack} disabled={isLoading}>
								<ArrowLeft class="mr-2 h-4 w-4" />
								Back
							</Button>
						</form>
					{/if}
				</CardContent>
			</Card>
		</div>
	{:else if accessStep === 'viewing' && imageData}
		<div class="relative min-h-screen">
			<!-- Main Image -->
			<div class="absolute inset-0">
				<img
					src={imageData.image_url}
					alt="Shared content"
					class="h-full w-full object-contain"
					on:contextmenu={(e) => e.preventDefault()}
				/>
			</div>

			<!-- Action Buttons -->
			<div class="absolute right-6 top-6 z-50 flex gap-2">
				<Button variant="secondary" class="bg-background/90 backdrop-blur-sm" on:click={toggleInfo}>
					{#if showInfo}
						<X class="h-5 w-5" />
					{:else}
						<Eye class="h-5 w-5" />
					{/if}
				</Button>
			</div>

			<!-- Info Panel -->
			{#if showInfo}
				<div
					class="absolute right-0 top-0 h-full w-80 space-y-6 border-l border-border bg-background/95 p-6 backdrop-blur-sm"
					transition:slide
				>
					<div class="space-y-4">
						{#if imageData.allow_download}
							<Button class="w-full" variant="outline" on:click={handleDownload}>
								<Download class="mr-2 h-5 w-5" />
								Download
							</Button>
						{/if}
						<Button class="w-full" variant="outline" on:click={handleShare}>
							<Share2 class="mr-2 h-5 w-5" />
							Share Link
						</Button>
					</div>

					<div class="space-y-2">
						<h3 class="font-semibold">Access Information</h3>
						<div class="space-y-1 text-sm text-muted-foreground">
							<p>Email: {email}</p>
							{#if imageData.max_views}
								<p>Views: {imageData.current_views} / {imageData.max_views}</p>
							{/if}
							<p>Access Type: {imageData.allow_download ? 'Full Access' : 'View Only'}</p>
						</div>
					</div>
				</div>
			{/if}
		</div>
	{:else}
		<div class="flex min-h-screen items-center justify-center p-4">
			<Alert variant="destructive" class="w-full max-w-md">
				<AlertTitle>Access Error</AlertTitle>
				<AlertDescription>Unable to load the requested content.</AlertDescription>
			</Alert>
		</div>
	{/if}
</div>

<style>
	/* Prevent image selection */
	img {
		user-select: none;
		-webkit-user-select: none;
		-moz-user-select: none;
		-ms-user-select: none;
	}
</style>
