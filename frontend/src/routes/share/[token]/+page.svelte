<script lang="ts">
	import { onMount } from 'svelte';
	import { browser } from '$app/environment';

	// UI Components
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import {
		Card,
		CardContent,
		CardHeader,
		CardTitle,
		CardDescription,
		CardFooter
	} from '$lib/components/ui/card';
	import { Alert, AlertDescription, AlertTitle } from '$lib/components/ui/alert';
	import { Label } from '$lib/components/ui/label';
	import {
		Dialog,
		DialogContent,
		DialogHeader,
		DialogFooter,
		DialogTitle,
		DialogDescription
	} from '$lib/components/ui/dialog';

	// Icons
	import {
		Lock,
		Download,
		Share2,
		X,
		Eye,
		Mail,
		Key,
		ArrowLeft,
		AlertCircle,
		CheckCircle2,
		Info,
		HelpCircle,
		Clock
	} from 'lucide-svelte';

	import { toast } from 'svelte-sonner';
	import { slide, fade } from 'svelte/transition';
	import { emailSchema, passwordSchema, otpSchema, accessRequestSchema } from './schema';

	export let data;

	let accessStep = 'email';
	let email = '';
	let password = '';
	let otp = '';
	let imageData = null;
	let showInfo = true;
	let isLoading = false;
	let accessFormError = '';
	let showRequestForm = false;
	let requestMessage = '';
	let isRequestPending = false;
	let apiResult = null;

	// Validation functions
	function validateEmail() {
		try {
			emailSchema.parse({ email });
			accessFormError = '';
			return true;
		} catch (error) {
			accessFormError = error.errors[0].message;
			return false;
		}
	}

	function validatePassword() {
		try {
			passwordSchema.parse({ password });
			accessFormError = '';
			return true;
		} catch (error) {
			accessFormError = error.errors[0].message;
			return false;
		}
	}

	function validateOTP() {
		try {
			otpSchema.parse({ otp });
			accessFormError = '';
			return true;
		} catch (error) {
			accessFormError = error.errors[0].message;
			return false;
		}
	}

	function validateAccessRequest() {
		try {
			accessRequestSchema.parse({ email, message: requestMessage });
			accessFormError = '';
			return true;
		} catch (error) {
			accessFormError = error.errors[0].message;
			return false;
		}
	}

	function openRequestForm() {
		if (apiResult?.request_status === 'pending') {
			toast.error('You already have a pending access request');
			return;
		}
		showRequestForm = true;
		toast.info('Please provide a reason for requesting access');
	}

	async function handleEmailSubmit() {
		if (!validateEmail() || !browser) return;

		isLoading = true;
		try {
			const response = await fetch(`/api/access/${data.token}/initiate/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ email })
			});

			const result = await response.json();
			console.log('Email submit result:', result);

			if (response.status === 403) {
				apiResult = result;
				// Handle the case where there's an existing request
				if (result.error?.includes('pending')) {
					toast.info('Access Request Pending');
					accessFormError = result.error;
					showRequestForm = false;
				} else {
					toast.warning(result.error);
					accessFormError = 'You are not authorized. Please request access from the owner.';
				}
				return;
			}

			if (!response.ok) {
				throw new Error(result.error || 'Failed to verify email');
			}

			// Handle successful response
			if (result.requires_password) {
				accessStep = 'password';
				toast.info('Password required for access');
				accessFormError = '';
			} else {
				accessStep = 'otp';
				toast.success('Verification code sent to your email');
				accessFormError = '';
			}
		} catch (error) {
			handleError(error);
		} finally {
			isLoading = false;
		}
	}

	function updateRequestStatus(status: string, message: string) {
		apiResult = { ...apiResult, request_status: status };
		accessFormError = message;
		showRequestForm = false;
	}

	async function handleRequestAccess() {
		if (!validateAccessRequest() || isRequestPending) return;

		isRequestPending = true;
		try {
			const response = await fetch(`/api/access/${data.token}/request/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ email, message: requestMessage })
			});

			const result = await response.json();

			if (response.status === 403) {
				if (result.request_status === 'pending') {
					toast.info('Request Already Pending');
					accessFormError = 'You already have a pending access request';
					showRequestForm = false;
				} else if (result.request_status === 'denied') {
					toast.error('Previous Request Denied');
					accessFormError = 'Your previous request was denied. You may submit a new request.';
				}
			} else if (response.status === 201 || response.status === 200) {
				// Successful submission
				toast.success(result.message || 'Request submitted successfully');
				showRequestForm = false;
				accessFormError = result.message;
				apiResult = { ...apiResult, request_status: 'pending' };
			} else {
				throw new Error(result.error || 'Failed to submit request');
			}
		} catch (error) {
			toast.error('Failed to submit request');
			accessFormError = error.message;
		} finally {
			isRequestPending = false;
		}
	}

	async function handleOTPSubmit() {
		if (!validateOTP() || !browser) return;

		isLoading = true;
		try {
			const response = await fetch(`/api/access/${data.token}/verify/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
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
			handleError(error);
		} finally {
			isLoading = false;
		}
	}

	function handleError(error) {
		console.error('Error:', error);
		accessFormError = error.message || 'An unexpected error occurred';
		toast.error(accessFormError);
	}

	function handleDownload() {
		if (!browser || !imageData?.allow_download) return;
		const link = document.createElement('a');
		link.href = imageData.image_url;
		link.download = '';
		document.body.appendChild(link);
		link.click();
		document.body.removeChild(link);
		toast.success('Downloading image...');
	}

	function handleShare() {
		if (!browser) return;
		navigator.clipboard.writeText(window.location.href);
		toast.success('Link copied to clipboard');
	}

	function toggleInfo() {
		showInfo = !showInfo;
	}

	function goBack() {
		if (accessStep === 'password') {
			password = '';
			accessStep = 'email';
		} else if (accessStep === 'otp') {
			otp = '';
			accessStep = password ? 'password' : 'email';
		}
		accessFormError = '';
	}
</script>

{#if showRequestForm}
	<Dialog open={showRequestForm} onOpenChange={(open: boolean) => (showRequestForm = open)}>
		<DialogContent class="border-2 sm:max-w-md">
			<DialogHeader class="pt-2">
				<div class="flex items-start space-x-4">
					<div
						class="flex h-12 w-12 items-center justify-center rounded-full bg-primary/10 text-primary"
					>
						<Mail class="h-6 w-6" />
					</div>
					<div class="space-y-1">
						<DialogTitle class="text-xl font-semibold">Request Access</DialogTitle>
						<DialogDescription>
							Submit a request to access this protected content. The owner will be notified.
						</DialogDescription>
					</div>
				</div>
			</DialogHeader>

			<form class="space-y-6 py-4" on:submit|preventDefault={handleRequestAccess}>
				<div class="space-y-2">
					<Label>Current Email</Label>
					<div class="rounded-md bg-muted p-3">
						<div class="flex items-center gap-2">
							<Mail class="h-4 w-4 text-muted-foreground" />
							<span class="text-sm font-medium">{email}</span>
						</div>
					</div>
				</div>

				<div class="space-y-2">
					<Label for="message">Message for Owner</Label>
					<textarea
						id="message"
						class="min-h-[120px] w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2"
						placeholder="Explain why you need access to this content..."
						bind:value={requestMessage}
					/>
				</div>

				<DialogFooter>
					<div class="flex w-full flex-col gap-2 sm:flex-row sm:justify-end">
						<Button
							type="button"
							variant="outline"
							on:click={() => (showRequestForm = false)}
							class="sm:w-auto"
						>
							Cancel
						</Button>
						<Button type="submit" disabled={isRequestPending} class="sm:w-auto">
							{#if isRequestPending}
								<div class="mr-2 h-4 w-4 animate-spin rounded-full border-b-2 border-white" />
								Submitting...
							{:else}
								Submit Request
							{/if}
						</Button>
					</div>
				</DialogFooter>
			</form>
		</DialogContent>
	</Dialog>
{/if}

<!-- Main Content -->
<div class="container mx-auto flex min-h-screen max-w-md items-center px-4 py-8 sm:px-6 lg:px-8">
	{#if ['email', 'password', 'otp'].includes(accessStep)}
		<Card class="w-full border-2 shadow-lg">
			<CardHeader class="space-y-4 pb-6 text-center">
				<div
					class="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-primary/10 ring-1 ring-primary/25"
				>
					<Lock class="h-8 w-8 text-primary" />
				</div>
				<div class="space-y-1.5">
					<CardTitle class="text-2xl font-bold tracking-tight">Protected Content</CardTitle>
					<CardDescription class="text-base">
						{#if accessStep === 'email'}
							Please verify your email to continue
						{:else if accessStep === 'password'}
							This content requires a password
						{:else if accessStep === 'otp'}
							Enter the verification code
						{/if}
					</CardDescription>
				</div>
			</CardHeader>

			<CardContent class="space-y-6">
				<!-- Access Request Button -->
				{#if accessStep === 'email' && !accessFormError?.includes('pending')}
					<div class="flex justify-center">
						<Button
							variant="outline"
							class="w-full max-w-sm gap-2 rounded-full hover:bg-primary/5"
							on:click={openRequestForm}
						>
							<Mail class="h-4 w-4" />
							Request Access
						</Button>
					</div>
				{/if}

				<!-- Error/Status Messages -->
				{#if accessFormError}
					<div transition:slide={{ duration: 200 }}>
						<Alert
							variant={accessFormError.includes('pending')
								? 'info'
								: accessFormError.includes('denied')
									? 'destructive'
									: 'warning'}
						>
							<div class="flex items-center gap-2">
								{#if accessFormError.includes('pending')}
									<Clock class="h-4 w-4" />
								{:else if accessFormError.includes('denied')}
									<X class="h-4 w-4" />
								{:else}
									<AlertCircle class="h-4 w-4" />
								{/if}
								<AlertDescription>{accessFormError}</AlertDescription>
							</div>
						</Alert>
					</div>
				{/if}

				<!-- Forms -->
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

						<Button type="submit" class="w-full" disabled={!email || isLoading}>
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

						<div class="flex flex-col gap-2">
							<Button type="submit" disabled={!password || isLoading}>
								{#if isLoading}
									<div class="mr-2 h-4 w-4 animate-spin rounded-full border-b-2 border-white" />
								{/if}
								Verify Password
							</Button>
							<Button variant="ghost" on:click={goBack} disabled={isLoading}>
								<ArrowLeft class="mr-2 h-4 w-4" />
								Back
							</Button>
						</div>
					</form>
				{:else if accessStep === 'otp'}
					<form class="space-y-4" on:submit|preventDefault={handleOTPSubmit}>
						<div class="space-y-2">
							<Label for="otp">Verification Code</Label>
							<Input
								id="otp"
								type="text"
								placeholder="000000"
								class="text-center font-mono text-lg tracking-[0.5em]"
								bind:value={otp}
								disabled={isLoading}
								maxlength="6"
							/>
							<p class="text-center text-sm text-muted-foreground">
								Enter the 6-digit code sent to {email}
							</p>
						</div>

						<div class="flex flex-col gap-2">
							<Button type="submit" disabled={!otp || isLoading}>
								{#if isLoading}
									<div class="mr-2 h-4 w-4 animate-spin rounded-full border-b-2 border-white" />
								{/if}
								Verify Code
							</Button>
							<Button variant="ghost" on:click={goBack} disabled={isLoading}>
								<ArrowLeft class="mr-2 h-4 w-4" />
								Back
							</Button>
						</div>
					</form>
				{/if}
			</CardContent>
		</Card>
	{:else if accessStep === 'viewing' && imageData}
		<!-- Protected Image Viewing Section -->
		<div class="relative w-full rounded-lg bg-background shadow-xl">
			<div class="absolute right-4 top-4 z-10 flex items-center gap-2">
				{#if imageData.allow_download}
					<Button variant="secondary" size="icon" on:click={handleDownload}>
						<Download class="h-4 w-4" />
					</Button>
				{/if}
				<Button variant="secondary" size="icon" on:click={handleShare}>
					<Share2 class="h-4 w-4" />
				</Button>
			</div>

			<img
				src={imageData.image_url}
				alt="Protected Content"
				class="w-full rounded-lg"
				style="pointer-events: none"
			/>
		</div>
	{:else}
		<Alert variant="destructive" class="w-full">
			<AlertCircle class="h-4 w-4" />
			<AlertTitle>Access Error</AlertTitle>
			<AlertDescription>Unable to load the protected content.</AlertDescription>
		</Alert>
	{/if}
</div>

<style>
	:global(body) {
		overflow-y: auto;
	}

	:global(body.modal-open) {
		overflow: hidden;
	}

	img {
		user-select: none;
		-webkit-user-select: none;
		-moz-user-select: none;
		-ms-user-select: none;
	}
</style>
