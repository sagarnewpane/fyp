<script lang="ts">
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
	import { Textarea } from '$lib/components/ui/textarea';
	import { Label } from '$lib/components/ui/label';
	import { Camera, Twitter, Instagram, Globe } from 'lucide-svelte';
	import { Separator } from '$lib/components/ui/separator';

	let username = $state('johndoe');
	let name = $state('John Doe');
	let email = $state('john@example.com');
	let avatarUrl = $state('');
	let socialLinks = $state({
		website: 'https://johndoe.com',
		twitter: '@johndoe',
		instagram: '@johndoe.photos'
	});

	function handleAvatarChange() {
		// Implement avatar change logic
	}

	function handleSubmit() {
		// Implement save changes logic
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
				<CardDescription
					>This information will be shown to users requesting access to your protected images</CardDescription
				>
			</CardHeader>
			<CardContent>
				<form on:submit|preventDefault={handleSubmit} class="space-y-8">
					<div class="flex flex-col items-start gap-6 sm:flex-row sm:items-center">
						<div class="group relative">
							<Avatar
								class="h-24 w-24 ring-2 ring-offset-2 ring-offset-background transition-all group-hover:ring-primary"
							>
								<AvatarImage src={avatarUrl} alt="Profile" />
								<AvatarFallback
									>{name
										.split(' ')
										.map((n) => n[0])
										.join('')}</AvatarFallback
								>
							</Avatar>
							<Button
								variant="outline"
								size="icon"
								class="absolute bottom-0 right-0 rounded-full shadow-lg"
								on:click={handleAvatarChange}
							>
								<Camera class="h-4 w-4" />
							</Button>
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
							<Input id="username" bind:value={username} placeholder="Enter your username" />
							<p class="text-sm text-muted-foreground">
								This is your unique identifier for the platform
							</p>
						</div>

						<div class="grid gap-2">
							<Label for="name">Display Name</Label>
							<Input id="name" bind:value={name} placeholder="Enter your full name" />
						</div>

						<div class="grid gap-2">
							<Label for="email">Email Address</Label>
							<Input id="email" type="email" bind:value={email} placeholder="Enter your email" />
							<p class="text-sm text-muted-foreground">
								Used for notifications and account recovery
							</p>
						</div>

						<Separator />

						<div class="space-y-4">
							<h3 class="font-medium">Social Links</h3>
							<div class="grid gap-4">
								<div class="grid gap-2">
									<Label class="flex items-center gap-2">
										<Globe class="h-4 w-4" /> Website
									</Label>
									<Input bind:value={socialLinks.website} placeholder="https://your-website.com" />
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
							</div>
						</div>
					</div>

					<div class="flex justify-end gap-4">
						<Button variant="outline" type="button">Cancel</Button>
						<Button type="submit">Save Changes</Button>
					</div>
				</form>
			</CardContent>
		</Card>
	</div>
</div>
