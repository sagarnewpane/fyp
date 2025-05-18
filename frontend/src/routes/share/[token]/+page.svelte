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
		Clock,
		Shield
	} from 'lucide-svelte';

	import { toast } from 'svelte-sonner';
	import { slide, fade } from 'svelte/transition';
	import { emailSchema, passwordSchema, otpSchema, accessRequestSchema } from './schema';

	export let data: { token: string };

	interface ImageData {
		image_url: string;
		allow_download: boolean;
		protection_features: {
			watermark: boolean;
			hidden_watermark: boolean;
			metadata: boolean;
			ai_protection: boolean;
		};
	}

	let accessStep = 'email';
	let email = '';
	let password = '';
	let otp = '';
	let imageData: ImageData | null = null;
	let showInfo = true;
	let isLoading = false;
	let accessFormError = '';
	let showRequestForm = false;
	let requestMessage = '';
	let isRequestPending = false;
	let apiResult: { request_status?: string } | null = null;
	let showProtectionInfo = false;
	let imageLoaded = false;

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

	// Security functions
	function handleContextMenu(event: MouseEvent) {
		event.preventDefault();
		toast.warning('Right-click is disabled for image protection');
		return false;
	}

	function handleImageLoad() {
		imageLoaded = true;
	}

	function getProtectionFeatures() {
		if (!imageData?.protection_features) return [];

		const features = [];
		const pf = imageData.protection_features;

		if (pf.watermark) features.push('Visible Watermark');
		if (pf.hidden_watermark) features.push('Hidden Watermark');
		if (pf.metadata) features.push('Protected Metadata');
		if (pf.ai_protection) features.push('AI Protection');
		if (!imageData.allow_download) features.push('Download Restricted');

		return features;
	}

	async function handleRequestAccess(event: Event) {
		event.preventDefault();
		if (!validateAccessRequest()) return;

		isRequestPending = true;
		try {
			const response = await fetch(`/api/access/${data.token}/request/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ email, message: requestMessage })
			});

			const result = await response.json();

			if (!response.ok) {
				throw new Error(result.error || 'Failed to submit access request');
			}

			showRequestForm = false;
			toast.success('Access request submitted successfully');
			accessFormError = 'Your access request is pending approval.';
		} catch (error) {
			handleError(error);
		} finally {
			isRequestPending = false;
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

	async function handlePasswordSubmit() {
		if (!validatePassword() || !browser) return;

		isLoading = true;
		try {
			const response = await fetch(`/api/access/${data.token}/initiate/`, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ email, password })
			});

			const result = await response.json();

			if (!response.ok) {
				throw new Error(result.error || 'Invalid password');
			}

			accessStep = 'otp';
			toast.success('Verification code sent to your email');
			accessFormError = '';
		} catch (error) {
			handleError(error);
		} finally {
			isLoading = false;
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

	function handleError(error: unknown) {
		console.error('Error:', error);
		accessFormError = error instanceof Error ? error.message : 'An unexpected error occurred';
		toast.error(accessFormError);
	}

	function handleDownload() {
		if (!browser || !imageData?.allow_download) return;
		
		// Show loading toast
		toast.loading('Preparing download...');
		
		fetch(`/api/access/${data.token}/download/`, {
			headers: {
				'X-Access-Email': email || 'unknown',
				'X-Access-Name': 'shared_access'
			}
		})
			.then(async response => {
				if (!response.ok) {
					throw new Error('Download failed');
				}
				const blob = await response.blob();
				const url = window.URL.createObjectURL(blob);
				const a = document.createElement('a');
				a.style.display = 'none';
				a.href = url;
				
				// Get filename from Content-Disposition header or use default
				const contentDisposition = response.headers.get('content-disposition');
				let filename = 'protected_image.png';
				if (contentDisposition) {
					const filenameMatch = contentDisposition.match(/filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/);
					if (filenameMatch && filenameMatch[1]) {
						filename = filenameMatch[1].replace(/['"]/g, '');
					}
				}
				a.download = filename;
				
				document.body.appendChild(a);
				a.click();
				window.URL.revokeObjectURL(url);
				a.remove();
				
				toast.success('Download started');
			})
			.catch((error: unknown) => {
				console.error('Download error:', error);
				toast.error(error instanceof Error ? error.message : 'Failed to download image');
			});
	}

	function handleShare() {
		if (!browser) return;
		navigator.clipboard.writeText(window.location.href);
		toast.success('Link copied to clipboard');
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

	onMount(() => {
		document.addEventListener('contextmenu', handleContextMenu);
		return () => {
			document.removeEventListener('contextmenu', handleContextMenu);
		};
	});
</script>

<svelte:head>
	{#if accessStep === 'viewing'}
		<style>
			img {
				-webkit-user-drag: none;
				-khtml-user-drag: none;
				-moz-user-drag: none;
				-o-user-drag: none;
				user-drag: none;
			}
		</style>
	{/if}
</svelte:head>

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
<div class="container mx-auto min-h-screen px-4 py-8 sm:px-6 lg:px-8">
	{#if ['email', 'password', 'otp'].includes(accessStep)}
		<Card class="mx-auto w-full max-w-md border-2 shadow-lg">
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
		<div class="mx-auto max-w-4xl space-y-6">
			<!-- Protection Info Banner -->
			<div class="rounded-lg bg-muted/50 p-4 backdrop-blur-sm">
				<div class="flex items-start gap-4">
					<div class="rounded-full bg-primary/10 p-2">
						<Shield class="h-5 w-5 text-primary" />
					</div>
					<div class="flex-1 space-y-1">
						<h3 class="text-sm font-medium">Protected Content</h3>
						<p class="text-sm text-muted-foreground">
							This image is protected with multiple security features.
							<button
								class="inline-flex items-center gap-1 text-primary hover:underline"
								on:click={() => (showProtectionInfo = !showProtectionInfo)}
							>
								<Info class="h-3 w-3" />
								{showProtectionInfo ? 'Hide Details' : 'View Details'}
							</button>
						</p>

						{#if showProtectionInfo}
							<div class="mt-3 space-y-2" transition:slide>
								<div class="flex flex-wrap gap-2">
									{#each getProtectionFeatures() as feature}
										<span
											class="rounded-full bg-primary/10 px-2 py-1 text-xs font-medium text-primary"
										>
											{feature}
										</span>
									{/each}
								</div>
								<p class="text-xs text-muted-foreground">
									This image is monitored and protected against unauthorized usage. Any attempt to
									circumvent these protections may be logged.
								</p>
							</div>
						{/if}
					</div>
				</div>
			</div>

			<!-- Image Container -->
			<div class="relative overflow-hidden rounded-lg bg-background shadow-xl">
				<!-- Loading State -->
				{#if !imageLoaded}
					<div class="absolute inset-0 flex items-center justify-center bg-background">
						<div
							class="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent"
						/>
					</div>
				{/if}

				<!-- Action Buttons -->
				<div class="absolute right-4 top-4 z-10 flex items-center gap-2 backdrop-blur-sm">
					{#if imageData.allow_download}
						<Button variant="secondary" size="icon" on:click={handleDownload}>
							<Download class="h-4 w-4" />
						</Button>
					{/if}
					<Button variant="secondary" size="icon" on:click={handleShare}>
						<Share2 class="h-4 w-4" />
					</Button>
				</div>

				<!-- Protected Image -->
				<div class="relative" style="contain: paint;">
					<img
						src={imageData.image_url}
						alt="Protected Content"
						class="w-full select-none"
						style="pointer-events: none; -webkit-user-select: none; -webkit-touch-callout: none;"
						on:load={handleImageLoad}
						draggable="false"
					/>

					<!-- Invisible overlay to prevent selection -->
					<div class="absolute inset-0" style="background: transparent;" />
				</div>
			</div>

			<!-- Additional Info -->
			<div class="text-center">
				<p class="text-sm text-muted-foreground">
					Having trouble accessing the content?
					<button
						class="text-primary hover:underline"
						on:click={() => {
							accessStep = 'email';
							imageData = null;
							imageLoaded = false;
						}}
					>
						Try again
					</button>
				</p>
			</div>
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
		-webkit-user-select: none;
		-moz-user-select: none;
		-ms-user-select: none;
		user-select: none;
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

	:global(body) {
		overflow-y: auto;
		-webkit-user-select: none;
		-moz-user-select: none;
		-ms-user-select: none;
		user-select: none;
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
