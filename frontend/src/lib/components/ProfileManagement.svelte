<script>
	import {
		Card,
		CardContent,
		CardHeader,
		CardTitle,
		CardDescription
	} from '$lib/components/ui/card';
	import { Input } from '$lib/components/ui/input';
	import { Button } from '$lib/components/ui/button';
	import { Avatar, AvatarImage, AvatarFallback } from '$lib/components/ui/avatar';
	import { Label } from '$lib/components/ui/label';
	import { Camera, Twitter, Instagram, Globe } from 'lucide-svelte';
	import { Separator } from '$lib/components/ui/separator';
	import { Skeleton } from '$lib/components/ui/skeleton';
	import { Alert, AlertDescription } from '$lib/components/ui/alert';
	import { AlertCircle } from 'lucide-svelte';
	import { avatarSchema, profileSchema } from '$lib/schemas';
	import { onMount } from 'svelte';
	import { toast } from 'svelte-sonner';
	import { authStore } from '$lib/stores/auth';

	// State variables
	let username = $state('');
	let firstName = $state('');
	let lastName = $state('');
	let email = $state('');
	let avatarUrl = $state('');
	let socialLinks = $state({
		website: '',
		twitter: '',
		instagram: ''
	});
	let isLoading = $state(true);
	let isUploading = $state(false);
	let selectedFile = $state(null);
	let fileInput;

	let fieldErrors = $state({});

	// Track original values for change detection
	let originalValues = $state(null);

	onMount(async () => {
		try {
			isLoading = true; // Set loading state
			const response = await fetch('/api/profile');
			if (response.ok) {
				const data = await response.json();
				username = data.username;
				firstName = data.first_name;
				lastName = data.last_name;
				email = data.email;
				avatarUrl = data.avatar_url;
				socialLinks = {
					website: data.social_links?.website || '',
					twitter: data.social_links?.twitter || '',
					instagram: data.social_links?.instagram || ''
				};
				originalValues = {
					username,
					first_name: firstName,
					last_name: lastName,
					email,
					social_links: { ...socialLinks }
				};
			}
		} catch (error) {
			console.error('Failed to fetch profile:', error);
			toast.error('Failed to load profile data');
		} finally {
			isLoading = false; // Clear loading state
		}
	});

	function handleAvatarClick() {
		if (!isUploading) {
			fileInput?.click();
		}
	}

	function handleAvatarChange(event) {
		selectedFile = event.target.files[0];
		if (selectedFile) {
			const reader = new FileReader();
			reader.onload = (e) => {
				avatarUrl = e.target.result; // Show preview
			};
			reader.readAsDataURL(selectedFile);
		}
	}

	function getInitials(firstName = '', lastName = '') {
		return `${firstName[0] || ''}${lastName[0] || ''}`.toUpperCase() || '?';
	}

	function hasOtherChanges() {
		if (!originalValues) return false;

		return (
			username !== originalValues.username ||
			firstName !== originalValues.first_name ||
			lastName !== originalValues.last_name ||
			email !== originalValues.email ||
			JSON.stringify(socialLinks) !== JSON.stringify(originalValues.social_links)
		);
	}

	async function handleSubmit(event) {
		event.preventDefault();
		fieldErrors = {}; // Reset errors

		if (!selectedFile && !hasOtherChanges()) {
			toast.error('No changes to save');
			return;
		}

		try {
			isUploading = true;
			const loadingToastId = toast.loading('Saving changes...');

			// Handle avatar upload if there's a new file
			if (selectedFile) {
				const avatarValidation = avatarSchema.safeParse({ file: selectedFile });
				if (!avatarValidation.success) {
					toast.dismiss(loadingToastId);
					toast.error(avatarValidation.error.errors[0].message);
					return;
				}

				const formData = new FormData();
				formData.append('avatar', selectedFile);

				const avatarResponse = await fetch('/api/profile/avatar', {
					method: 'POST',
					body: formData
				});

				if (!avatarResponse.ok) {
					toast.dismiss(loadingToastId);
					toast.error('Failed to upload avatar');
					return;
				}

				const avatarData = await avatarResponse.json();
				const newAvatarUrl = avatarData.avatar_url + '?t=' + new Date().getTime();
				avatarUrl = newAvatarUrl;
				authStore.update((state) => ({
					...state,
					avatar: newAvatarUrl
				}));
			}

			// Handle other profile updates
			if (hasOtherChanges()) {
				const profileData = {
					username,
					first_name: firstName,
					last_name: lastName,
					email,
					social_links: socialLinks
				};

				const profileValidation = profileSchema.safeParse(profileData);
				if (!profileValidation.success) {
					toast.dismiss(loadingToastId);
					profileValidation.error.errors.forEach((error) => {
						fieldErrors[error.path[0]] = error.message;
					});
					toast.error('Please fix the validation errors');
					return;
				}

				const profileResponse = await fetch('/api/profile/', {
					method: 'PATCH',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify(profileData)
				});

				const responseData = await profileResponse.json();

				if (!profileResponse.ok) {
					toast.dismiss(loadingToastId);
					// Handle backend validation errors
					console.log(responseData);
					if (responseData && typeof responseData === 'object') {
						Object.keys(responseData).forEach((key) => {
							fieldErrors[key] = responseData[key][0];
						});
						toast.error('Please fix the validation errors');
					} else {
						toast.error('Failed to update profile');
					}
					return;
				}

				// Update original values after successful save
				originalValues = { ...profileData };
			}

			toast.dismiss(loadingToastId);
			toast.success('Changes saved successfully');

			selectedFile = null;
			if (fileInput) fileInput.value = '';
		} catch (error) {
			console.error('Save error:', error);
			toast.error(error.message || 'Failed to save changes');
		} finally {
			isUploading = false;
		}
	}
</script>

<div class="container mx-auto max-w-4xl px-4 py-8">
	<div class="space-y-8">
		<div>
			<h2 class="text-3xl font-bold tracking-tight">Profile Settings</h2>
			<p class="mt-2 text-muted-foreground">Manage your public profile and connected accounts</p>
		</div>

		<Card>
			<CardHeader>
				<CardTitle>Public Profile</CardTitle>
				<CardDescription>
					This information will be shown to users requesting access to your protected images
				</CardDescription>
			</CardHeader>
			<CardContent>
				<form on:submit={handleSubmit} class="space-y-8">
					<div class="flex flex-col items-start gap-6 sm:flex-row sm:items-center">
						<div class="group relative">
							{#if isLoading}
								<Skeleton class="h-24 w-24 rounded-full" />
							{:else}
								<Avatar
									class="h-24 w-24 cursor-pointer ring-2 ring-offset-2 ring-offset-background transition-all group-hover:ring-primary {isUploading
										? 'opacity-50'
										: ''}"
									on:click={handleAvatarClick}
								>
									{#if avatarUrl}
										<AvatarImage
											src={avatarUrl}
											alt="Profile"
											on:error={() => {
												avatarUrl = '';
											}}
										/>
									{/if}
									<AvatarFallback>{getInitials(firstName, lastName)}</AvatarFallback>
								</Avatar>
							{/if}
							<Button
								variant="outline"
								size="icon"
								type="button"
								class="absolute bottom-0 right-0 rounded-full shadow-lg"
								on:click={handleAvatarClick}
								disabled={isUploading || isLoading}
							>
								<Camera class="h-4 w-4" />
							</Button>
							<input
								type="file"
								accept="image/*"
								class="hidden"
								bind:this={fileInput}
								on:change={handleAvatarChange}
								disabled={isUploading || isLoading}
							/>
						</div>
						<div class="flex-1 space-y-1">
							<h3 class="font-medium">Profile Picture</h3>
							<p class="text-sm text-muted-foreground">
								This will be displayed on your public profile
							</p>
						</div>
					</div>

					<div class="grid gap-6">
						<div class="grid gap-2">
							<Label for="username">Username</Label>
							{#if isLoading}
								<Skeleton class="h-10 w-full" />
							{:else}
								<div class="space-y-2">
									<Input
										id="username"
										bind:value={username}
										placeholder="Enter your username"
										class={fieldErrors.username ? 'border-destructive' : ''}
									/>
									{#if fieldErrors.username}
										<div class="flex items-center gap-2 text-sm text-destructive">
											<AlertCircle class="h-4 w-4" />
											<span>{fieldErrors.username}</span>
										</div>
									{/if}
								</div>
							{/if}
							<p class="text-sm text-muted-foreground">
								This is your unique identifier for the platform
							</p>
						</div>

						<div class="grid gap-2">
							<Label>Display Name</Label>
							{#if isLoading}
								<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
									<Skeleton class="h-10 w-full" />
									<Skeleton class="h-10 w-full" />
								</div>
							{:else}
								<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
									<div class="grid gap-2">
										<Label for="first-name" class="text-sm text-muted-foreground">First Name</Label>
										<div class="space-y-2">
											<Input
												id="first-name"
												bind:value={firstName}
												placeholder="Enter first name"
												class={fieldErrors.first_name ? 'border-destructive' : ''}
											/>
											{#if fieldErrors.first_name}
												<div class="flex items-center gap-2 text-sm text-destructive">
													<AlertCircle class="h-4 w-4" />
													<span>{fieldErrors.first_name}</span>
												</div>
											{/if}
										</div>
									</div>
									<div class="grid gap-2">
										<Label for="last-name" class="text-sm text-muted-foreground">Last Name</Label>
										<div class="space-y-2">
											<Input
												id="last-name"
												bind:value={lastName}
												placeholder="Enter last name"
												class={fieldErrors.last_name ? 'border-destructive' : ''}
											/>
											{#if fieldErrors.last_name}
												<div class="flex items-center gap-2 text-sm text-destructive">
													<AlertCircle class="h-4 w-4" />
													<span>{fieldErrors.last_name}</span>
												</div>
											{/if}
										</div>
									</div>
								</div>
							{/if}
						</div>

						<div class="grid gap-2">
							<Label for="email">Email Address</Label>
							{#if isLoading}
								<Skeleton class="h-10 w-full" />
							{:else}
								<div class="space-y-2">
									<Input
										id="email"
										type="email"
										bind:value={email}
										placeholder="Enter your email"
										class={fieldErrors.email ? 'border-destructive' : ''}
									/>
									{#if fieldErrors.email}
										<div class="flex items-center gap-2 text-sm text-destructive">
											<AlertCircle class="h-4 w-4" />
											<span>{fieldErrors.email}</span>
										</div>
									{/if}
								</div>
							{/if}
							<p class="text-sm text-muted-foreground">
								Used for notifications and account recovery
							</p>
						</div>

						<Separator />

						<div class="space-y-4">
							<h3 class="font-medium">Social Links</h3>
							<div class="grid gap-4">
								{#if isLoading}
									<Skeleton class="h-10 w-full" />
									<Skeleton class="h-10 w-full" />
									<Skeleton class="h-10 w-full" />
								{:else}
									<div class="grid gap-2">
										<Label class="flex items-center gap-2">
											<Globe class="h-4 w-4" /> Website
										</Label>
										<Input
											bind:value={socialLinks.website}
											placeholder="https://your-website.com"
										/>
									</div>

									<div class="grid gap-2">
										<Label class="flex items-center gap-2">
											<Twitter class="h-4 w-4" /> Twitter
										</Label>
										<Input bind:value={socialLinks.twitter} placeholder="@username" />
									</div>

									<div class="grid gap-2">
										<Label class="flex items-center gap-2">
											<Instagram class="h-4 w-4" /> Instagram
										</Label>
										<Input bind:value={socialLinks.instagram} placeholder="@username" />
									</div>
								{/if}
							</div>
						</div>
					</div>

					<div class="flex justify-end gap-4">
						<Button variant="outline" type="button" disabled={isUploading || isLoading}>
							Cancel
						</Button>
						<Button type="submit" disabled={isUploading || isLoading}>
							{#if isUploading}
								Saving...
							{:else}
								Save Changes
							{/if}
						</Button>
					</div>
				</form>
			</CardContent>
		</Card>
	</div>
</div>
