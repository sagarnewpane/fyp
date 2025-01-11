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
	let passwordErrors = $state({});
	let isChangingPassword = $state(false);

	async function updatePassword(event: Event) {
		event.preventDefault();
		passwordErrors = {};

		// Validate input
		const validation = passwordChangeSchema.safeParse(passwords);
		if (!validation.success) {
			validation.error.errors.forEach((error) => {
				passwordErrors[error.path[0]] = error.message;
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
						passwordErrors[key] = data[key];
					});
					toast.error('Please fix the validation errors');
				} else {
					toast.error('Failed to update password');
				}
				return;
			}

			// Clear form
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

	function saveSecurity() {
		// Implement security settings save logic
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
					<!-- Access Notifications -->
					<div class="flex items-center justify-between">
						<div class="space-y-0.5">
							<Label class="text-base">Access Request Notifications</Label>
							<p class="text-sm text-muted-foreground">
								Receive notifications when someone requests access
							</p>
						</div>
						<Switch checked={notifications.accessRequests} />
					</div>

					<!-- Download Alerts -->
					<div class="flex items-center justify-between">
						<div class="space-y-0.5">
							<Label class="text-base">Download Alerts</Label>
							<p class="text-sm text-muted-foreground">
								Get notified when your images are downloaded
							</p>
						</div>
						<Switch checked={notifications.downloadAlerts} />
					</div>

					<!-- Access Notifications -->
					<div class="flex items-center justify-between">
						<div class="space-y-0.5">
							<Label class="text-base">Successful Access Alerts</Label>
							<p class="text-sm text-muted-foreground">
								Notifications when someone successfully views your images
							</p>
						</div>
						<Switch checked={notifications.successfulAccess} />
					</div>

					<!-- Failed Attempts -->
					<div class="flex items-center justify-between">
						<div class="space-y-0.5">
							<Label class="text-base">Failed Access Attempts</Label>
							<p class="text-sm text-muted-foreground">
								Get alerted about unauthorized access attempts
							</p>
						</div>
						<Switch checked={notifications.failedAttempts} />
					</div>

					<!-- Weekly Summary -->
					<div class="flex items-center justify-between">
						<div class="space-y-0.5">
							<Label class="text-base">Weekly Activity Digest</Label>
							<p class="text-sm text-muted-foreground">
								Receive a weekly summary of all activities
							</p>
						</div>
						<Switch checked={notifications.weeklyDigest} />
					</div>
				</div>
			</CardContent>
		</Card>

		<!-- Security Settings -->
		<Card>
			<CardHeader>
				<CardTitle>Security Settings</CardTitle>
				<CardDescription>Manage your account security and access preferences</CardDescription>
			</CardHeader>
			<CardContent>
				<div class="space-y-6">
					<!-- 2FA -->
					<div class="flex items-center justify-between">
						<div class="space-y-0.5">
							<Label class="text-base">Two-Factor Authentication</Label>
							<p class="text-sm text-muted-foreground">
								Add an extra layer of security to your account
							</p>
						</div>
						<Switch checked={security.twoFactorAuth} />
					</div>

					<!-- Auto-approve verified -->
					<div class="flex items-center justify-between">
						<div class="space-y-0.5">
							<Label class="text-base">Auto-approve Verified Users</Label>
							<p class="text-sm text-muted-foreground">
								Automatically approve requests from verified users
							</p>
						</div>
						<Switch checked={security.autoApproveVerified} />
					</div>

					<!-- Require reason -->
					<div class="flex items-center justify-between">
						<div class="space-y-0.5">
							<Label class="text-base">Require Request Reason</Label>
							<p class="text-sm text-muted-foreground">
								Users must provide a reason for access requests
							</p>
						</div>
						<Switch checked={security.requireRequestReason} />
					</div>

					<!-- Unknown IP -->
					<div class="flex items-center justify-between">
						<div class="space-y-0.5">
							<Label class="text-base">Unknown IP Alerts</Label>
							<p class="text-sm text-muted-foreground">
								Get notified of access from new IP addresses
							</p>
						</div>
						<Switch checked={security.notifyUnknownIP} />
					</div>

					<Separator />

					<!-- Download Link Expiry -->
					<div class="space-y-4">
						<Label class="text-base">Download Link Expiry</Label>
						<p class="text-sm text-muted-foreground">Set how long download links remain active</p>
						<select
							class="w-full rounded-md border border-input bg-background px-3 py-2"
							bind:value={security.downloadExpiry}
						>
							<option value={12}>12 Hours</option>
							<option value={24}>24 Hours</option>
							<option value={48}>48 Hours</option>
							<option value={72}>72 Hours</option>
						</select>
					</div>
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
