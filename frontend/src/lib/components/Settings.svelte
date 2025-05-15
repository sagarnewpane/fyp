<script lang="ts">
	import {
		Card,
		CardContent,
		CardHeader,
		CardTitle,
		CardDescription
	} from '$lib/components/ui/card';
	import { Switch } from '$lib/components/ui/switch';
	import { Label } from '$lib/components/ui/label';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import {
		Bell,
		Mail,
		Lock,
		Shield,
		Eye,
		Download,
		Key,
		UserCheck,
		MessageSquare,
		AlertCircle
	} from 'lucide-svelte';
	import { Separator } from '$lib/components/ui/separator';
	import { passwordChangeSchema } from '$lib/schemas';
	import { toast } from 'svelte-sonner';
	import { onMount } from 'svelte';
	import { Skeleton } from '$lib/components/ui/skeleton';

	// Type for notification settings from backend
	type NotificationSettingsAPI = {
		notify_on_access_request: boolean;
		notify_on_download: boolean;
		notify_on_successful_access: boolean;
		notify_on_failed_access: boolean;
	};

	// State for notification settings
	let notificationSettings = $state<NotificationSettingsAPI | null>(null);
	let previousNotificationSettings = $state<NotificationSettingsAPI | null>(null); // For diffing
	let isLoadingNotifications = $state(true);
	let errorLoadingNotifications = $state<string | null>(null);

	// Notification preferences
	let notifications = $state({
		accessRequests: true,
		downloadAlerts: true,
		successfulAccess: true,
		failedAttempts: true,
		weeklyDigest: false
	});

	// Security settings
	let security = $state({
		twoFactorAuth: true,
		autoApproveVerified: false,
		requireRequestReason: true,
		notifyUnknownIP: true,
		downloadExpiry: 24 // hours
	});

	// Password state
	let passwords = $state({
		current_password: '',
		new_password: '',
		confirm_password: ''
	});
	let passwordErrors = $state<Record<string, string>>({}); // Initialized for linter
	let isChangingPassword = $state(false);

	// Fetch notification settings on mount
	onMount(async () => {
		try {
			isLoadingNotifications = true;
			const response = await fetch('/api/user/notification-settings');
			if (response.ok) {
				const data = await response.json();
				notificationSettings = data;
				previousNotificationSettings = JSON.parse(JSON.stringify(data)); 
			} else {
				const errorData = await response.json();
				errorLoadingNotifications = errorData.error || 'Failed to load notification settings.';
				if (errorLoadingNotifications) {
				    toast.error(errorLoadingNotifications);
				} else {
				    toast.error('Failed to load notification settings.'); 
				}
			}
		} catch (e) {
			console.error('Error fetching notification settings:', e);
			errorLoadingNotifications = 'An unexpected error occurred while loading settings.';
			toast.error(errorLoadingNotifications);
		} finally {
			isLoadingNotifications = false;
		}
	});

	// Effect to handle notification setting changes
	$effect(() => {
		if (isLoadingNotifications || !notificationSettings || !previousNotificationSettings) {
			return; 
		}

		let changedKey: keyof NotificationSettingsAPI | null = null;
		let newValue: boolean | undefined;
		let oldValue: boolean | undefined;

		for (const k in notificationSettings) {
			const key = k as keyof NotificationSettingsAPI;
			if (notificationSettings[key] !== previousNotificationSettings[key]) {
				changedKey = key;
				newValue = notificationSettings[key];
				oldValue = previousNotificationSettings[key];
				break; 
			}
		}

		if (changedKey && typeof newValue === 'boolean' && typeof oldValue === 'boolean') {
			const keyToUpdate = changedKey;
			const valueToUpdate = newValue;
			const valueToRevertTo = oldValue;

			previousNotificationSettings = JSON.parse(JSON.stringify(notificationSettings));

			(async () => {
				try {
					const response = await fetch('/api/user/notification-settings', {
						method: 'PATCH',
						headers: {
							'Content-Type': 'application/json'
						},
						body: JSON.stringify({ [keyToUpdate]: valueToUpdate })
					});

					if (response.ok) {
						const updatedFromServer = await response.json();
						notificationSettings = { ...notificationSettings, ...updatedFromServer }; 
                        previousNotificationSettings = JSON.parse(JSON.stringify(notificationSettings)); 
						toast.success('Notification setting updated!');
					} else {
						if (notificationSettings) notificationSettings[keyToUpdate] = valueToRevertTo;
						previousNotificationSettings = JSON.parse(JSON.stringify(notificationSettings)); 
						const errorData = await response.json();
						toast.error(errorData.error || 'Failed to update setting.');
					}
				} catch (e) {
					if (notificationSettings) notificationSettings[keyToUpdate] = valueToRevertTo;
					previousNotificationSettings = JSON.parse(JSON.stringify(notificationSettings)); 
					console.error('Error updating notification setting:', e);
					toast.error('An unexpected error occurred.');
				}
			})();
		} else if (notificationSettings && previousNotificationSettings && JSON.stringify(notificationSettings) !== JSON.stringify(previousNotificationSettings)) {
		    previousNotificationSettings = JSON.parse(JSON.stringify(notificationSettings));
		}
	});

	const preferenceItems = [
		{
			key: 'notify_on_access_request' as keyof NotificationSettingsAPI,
			label: 'Access Request Notifications',
			description: 'Receive notifications when someone requests access to your images.'
		},
		{
			key: 'notify_on_download' as keyof NotificationSettingsAPI,
			label: 'Download Alerts',
			description: 'Get notified when your images are downloaded.'
		},
		{
			key: 'notify_on_successful_access' as keyof NotificationSettingsAPI,
			label: 'Successful Access Alerts',
			description: 'Receive notifications when someone successfully views your images.'
		},
		{
			key: 'notify_on_failed_access' as keyof NotificationSettingsAPI,
			label: 'Failed Access Attempts',
			description: 'Get alerted about unauthorized access attempts to your images.'
		}
	];

	async function updatePassword(event: Event) {
		event.preventDefault();
		passwordErrors = {};

		const validation = passwordChangeSchema.safeParse(passwords);
		if (!validation.success) {
			validation.error.errors.forEach((error) => {
				if (typeof error.path[0] === 'string') { // Linter fix
 					passwordErrors[error.path[0]] = error.message;
 				}
			});
			toast.error('Please fix the validation errors');
			return;
		}

		try {
			isChangingPassword = true;
			const loadingToastId = toast.loading('Updating password...');

			const response = await fetch('/api/password/change/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(passwords)
			});

			const data = await response.json();

			if (!response.ok) {
				toast.dismiss(loadingToastId);
				if (data && typeof data === 'object') {
					Object.keys(data).forEach((key) => {
						if (typeof data[key] === 'string') { // Linter fix
 							passwordErrors[key] = data[key];
 						}
					});
					toast.error('Please fix the validation errors');
				} else {
					toast.error('Failed to update password');
				}
				return;
			}

			passwords.current_password = '';
			passwords.new_password = '';
			passwords.confirm_password = '';

			toast.dismiss(loadingToastId);
			toast.success('Password updated successfully');
		} catch (error) {
			console.error('Password update error:', error);
			toast.error('Failed to update password');
		} finally {
			isChangingPassword = false;
		}
	}

	function saveNotificationSettings() {
		// Implement notification settings save logic
	}

</script>

<div class="container mx-auto max-w-4xl px-4 py-8">
	<div class="space-y-8">
		<div>
			<h2 class="text-3xl font-bold tracking-tight">Security & Notifications</h2>
			<p class="mt-2 text-muted-foreground">
				Configure your account security and notification preferences
			</p>
		</div>

		<!-- Notification Settings -->
		<Card>
			<CardHeader>
				<CardTitle>Notification Preferences</CardTitle>
				<CardDescription
					>Control how you want to be notified about your protected images</CardDescription
				>
			</CardHeader>
			<CardContent>
				<div class="space-y-6">
					{#if isLoadingNotifications}
						{#each preferenceItems as item (item.key)} 
							<div class="flex items-center justify-between space-x-4 rounded-lg border p-4">
								<div class="space-y-0.5">
									<Skeleton class="h-5 w-48" />
									<Skeleton class="h-4 w-full max-w-xs" />
								</div>
								<Skeleton class="h-6 w-10 rounded-full" />
							</div>
						{/each}
					{:else if errorLoadingNotifications}
						<p class="text-destructive">{errorLoadingNotifications}</p>
					{:else if notificationSettings}
						{#each preferenceItems as item (item.key)}
							<div class="flex flex-row items-center justify-between space-x-4 rounded-lg border p-4">
								<div class="space-y-0.5">
									<Label for={item.key} class="text-base font-medium">
										{item.label}
									</Label>
									<p class="text-sm text-muted-foreground">{item.description}</p>
								</div>
								<Switch
									id={item.key}
									bind:checked={notificationSettings[item.key]}
								/>
							</div>
						{/each}
					{:else}
						<p>Could not load notification settings.</p>
					{/if}
				</div>
			</CardContent>
		</Card>

		<!-- Password Change -->
		<Card>
			<CardHeader>
				<CardTitle>Change Password</CardTitle>
				<CardDescription>Update your account password</CardDescription>
			</CardHeader>
			<CardContent>
				<form class="space-y-4" on:submit={updatePassword}>
					<div class="space-y-2">
						<Label for="current-password">Current Password</Label>
						<div class="space-y-2">
							<Input
								id="current-password"
								type="password"
								bind:value={passwords.current_password}
								class={passwordErrors.current_password ? 'border-destructive' : ''}
							/>
							{#if passwordErrors.current_password}
								<div class="flex items-center gap-2 text-sm text-destructive">
									<AlertCircle class="h-4 w-4" />
									<span>{passwordErrors.current_password}</span>
								</div>
							{/if}
						</div>
					</div>

					<div class="space-y-2">
						<Label for="new-password">New Password</Label>
						<div class="space-y-2">
							<Input
								id="new-password"
								type="password"
								bind:value={passwords.new_password}
								class={passwordErrors.new_password ? 'border-destructive' : ''}
							/>
							{#if passwordErrors.new_password}
								<div class="flex items-center gap-2 text-sm text-destructive">
									<AlertCircle class="h-4 w-4" />
									<span>{passwordErrors.new_password}</span>
								</div>
							{/if}
						</div>
					</div>

					<div class="space-y-2">
						<Label for="confirm-password">Confirm New Password</Label>
						<div class="space-y-2">
							<Input
								id="confirm-password"
								type="password"
								bind:value={passwords.confirm_password}
								class={passwordErrors.confirm_password ? 'border-destructive' : ''}
							/>
							{#if passwordErrors.confirm_password}
								<div class="flex items-center gap-2 text-sm text-destructive">
									<AlertCircle class="h-4 w-4" />
									<span>{passwordErrors.confirm_password}</span>
								</div>
							{/if}
						</div>
					</div>

					<div class="flex justify-end gap-4">
						<Button
							variant="outline"
							type="button"
							disabled={isChangingPassword}
							on:click={() => {
								passwords.current_password = '';
								passwords.new_password = '';
								passwords.confirm_password = '';
								passwordErrors = {};
							}}
						>
							Cancel
						</Button>
						<Button type="submit" disabled={isChangingPassword}>
							{#if isChangingPassword}
								Updating...
							{:else}
								Update Password
							{/if}
						</Button>
					</div>
				</form>
			</CardContent>
		</Card>
	</div>
</div>
