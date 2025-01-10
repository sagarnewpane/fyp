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
		MessageSquare
	} from 'lucide-svelte';
	import { Separator } from '$lib/components/ui/separator';

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

	// Password fields
	let passwords = $state({
		current: '',
		new: '',
		confirm: ''
	});

	function updatePassword() {
		// Implement password update logic
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
				<form class="space-y-4" on:submit|preventDefault={updatePassword}>
					<div class="space-y-2">
						<Label for="current-password">Current Password</Label>
						<Input id="current-password" type="password" bind:value={passwords.current} />
					</div>

					<div class="space-y-2">
						<Label for="new-password">New Password</Label>
						<Input id="new-password" type="password" bind:value={passwords.new} />
					</div>

					<div class="space-y-2">
						<Label for="confirm-password">Confirm New Password</Label>
						<Input id="confirm-password" type="password" bind:value={passwords.confirm} />
					</div>

					<Button type="submit" class="w-full">Update Password</Button>
				</form>
			</CardContent>
		</Card>
	</div>
</div>
