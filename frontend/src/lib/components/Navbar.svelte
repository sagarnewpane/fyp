<script lang="js">
	import { Menu, Shield, X, ChevronRight, Album, DollarSign, Contact, LogOut, User } from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';
	import { slide, fade } from 'svelte/transition';
	import { page } from '$app/stores';
	import { authStore } from '$lib/stores/auth';
	import { goto, invalidate } from '$app/navigation';
	import {
		DropdownMenu,
		DropdownMenuTrigger,
		DropdownMenuContent,
		DropdownMenuItem
	} from '$lib/components/ui/dropdown-menu';
	import { Avatar, AvatarImage, AvatarFallback } from '$lib/components/ui/avatar';
	import { fetchUserAvatar } from '$lib/utils/avatar';

	let currentPath = $derived($page.url.pathname);

	// const user = $derived($authStore?.user || null); // Old user derivation
	const isAuthenticated = $derived(Boolean($authStore?.isAuthenticated));
	const avatarUrl = $derived($authStore?.avatar || null);

	// Directly derive username and related properties from the store state
	const currentUsername = $derived($authStore?.user?.username || null);
	const userInitials = $derived(currentUsername?.[0]?.toUpperCase() ?? '?');
	const displayUsername = $derived(
	    currentUsername 
	        ? currentUsername.charAt(0).toUpperCase() + currentUsername.slice(1) 
	        : (isAuthenticated ? 'User' : '')
	);

	function handleAvatarError() {
		console.error('Failed to load avatar');
		authStore.update((state) => ({
			...state,
			avatar: null
		}));
	}

	async function loadAvatar() {
		if (isAuthenticated) {
			const fetchedAvatar = await fetchUserAvatar();
			if (fetchedAvatar) {
				authStore.update((state) => ({
					...state,
					avatar: fetchedAvatar
				}));
			}
		}
	}

	$effect(() => {
		if (isAuthenticated !== undefined) {
			loadAvatar();
		}
	});

	async function handleLogout() {
		const response = await fetch('/logout', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			}
		});
		invalidate('app:auth');
		isMobileMenuOpen = false;
	}

	const navItems = [
		{ label: 'Home', href: '/', icon: Shield },
		{ label: 'Images', href: '/images', icon: Album },
		{ label: 'Contact', href: '#', icon: Contact }
	];

	const dropItems = [{ label: 'Profile', href: '/user?tab=profile', icon: User }];

	let isMobileMenuOpen = $state(false);

	const toggleMobileMenu = () => {
		isMobileMenuOpen = !isMobileMenuOpen;
	};
</script>

<nav
	class="supports-[backdrop-filter]:bg-background/0.1 sticky top-0 z-50 w-full border-b bg-background/95 shadow-sm backdrop-blur"
>
	<div class="px-4">
		<div class="flex h-16 items-center justify-between">
			<!-- Logo and brand -->
			<div class="group flex items-center">
				<div
					class="flex h-8 w-8 items-center justify-center transition-transform duration-300 group-hover:scale-110"
				>
					<img src="/crop.png" alt="Authograph Logo" class="rounded-full shadow-sm" />
				</div>
				<a href="/">
					<span
						class="relative cursor-pointer text-xl font-semibold text-primary transition-colors duration-300
            after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 after:bg-primary
            after:transition-all after:duration-300 group-hover:after:w-full"
					>
						uthograph
					</span>
				</a>
			</div>

			<!-- Desktop navigation -->
			<div class="hidden md:flex md:items-center md:gap-4">
				{#each navItems as item}
					<a
						href={item.href}
						class="relative px-2 text-[#1A202C] transition-colors after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 after:bg-[#2B6CB0] after:transition-all after:duration-300 hover:text-[#2B6CB0] hover:after:w-full {currentPath ===
						item.href
							? 'text-[#2B6CB0] after:w-full'
							: ''}"
					>
						{item.label}
					</a>
				{/each}
			</div>

			<!-- Auth section (desktop) -->
			<div class="hidden items-center gap-2 md:flex">
				{#if isAuthenticated}
					<DropdownMenu>
						<div class="flex items-center gap-2">
							<DropdownMenuTrigger class="focus:outline-none">
								<Avatar
									class="border-2 border-primary/20 transition-all duration-300 hover:border-primary/50"
								>
									{#if avatarUrl}
										<AvatarImage src={avatarUrl} alt="User avatar" on:error={handleAvatarError} />
									{/if}
									<AvatarFallback>
										{userInitials}
									</AvatarFallback>
								</Avatar>
							</DropdownMenuTrigger>
						</div>
						<DropdownMenuContent
							align="end"
							class="w-48 rounded-md border bg-background p-1 shadow-lg"
						>
							{#each dropItems as item}
								<a href={item.href} class="block">
									<DropdownMenuItem class="flex w-full cursor-pointer items-center gap-2">
										<item.icon class="h-4 w-4 text-muted-foreground" />
										<span>{item.label}</span>
									</DropdownMenuItem>
								</a>
							{/each}

							<DropdownMenuItem
								class="flex w-full cursor-pointer items-center gap-2 text-destructive focus:bg-destructive focus:text-destructive-foreground"
								on:click={handleLogout}
							>
								<LogOut class="h-4 w-4" />
								<span>Logout</span>
							</DropdownMenuItem>
						</DropdownMenuContent>
					</DropdownMenu>
				{:else}
					<Button
						variant="ghost"
						class="relative overflow-hidden px-3 text-[#1A202C] transition-colors after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 after:bg-[#2B6CB0] after:transition-all after:duration-300 hover:text-[#2B6CB0] hover:after:w-full"
						href="/login">Login</Button
					>
					<Button
						class="bg-[#2B6CB0] px-4 py-2 text-white transition-transform duration-300 hover:scale-105 hover:bg-[#235A94] hover:shadow-lg hover:shadow-[#2B6CB0]/20"
						href="/register">Register</Button
					>
				{/if}
			</div>

			<!-- Mobile menu button -->
			<Button
				variant="ghost"
				size="icon"
				on:click={toggleMobileMenu}
				class="relative transition-all duration-300 after:absolute
           after:bottom-0 after:left-0 after:h-[2px] after:w-0
           after:bg-primary after:transition-all after:duration-300 hover:bg-primary/5
           hover:after:w-full md:hidden"
			>
				{#if isMobileMenuOpen}
					<div in:fade={{ duration: 200 }}>
						<X class="h-5 w-5" />
					</div>
				{:else}
					<div in:fade={{ duration: 200 }}>
						<Menu class="h-5 w-5" />
					</div>
				{/if}
			</Button>
		</div>
	</div>

	<!-- Mobile navigation -->
	{#if isMobileMenuOpen}
		<div
			class="supports-[backdrop-filter]:bg-background/0.1 fixed left-0 top-16 z-40 h-[calc(100vh-4rem)] w-full border-t bg-background/95 backdrop-blur md:hidden"
			transition:slide={{ duration: 200 }}
		>
			<div class="container mx-auto px-4 py-4">
				<div class="flex flex-col gap-4">
					{#if isAuthenticated}
						<div class="flex items-center gap-3 px-3 py-2">
							<Avatar>
								{#if avatarUrl}
									<AvatarImage src={avatarUrl} alt="User avatar" />
								{/if}
								<AvatarFallback>
									{userInitials}
								</AvatarFallback>
							</Avatar>
							<span class="text-xl font-semibold">
								{displayUsername}
							</span>
						</div>
						<!-- Mobile items from drop Down-->
						{#each dropItems as item}
							<a
								href={item.href}
								class="group relative flex items-center justify-between rounded-md px-3 py-2 transition-all hover:bg-primary/5 active:scale-[0.98]"
								onclick={() => (isMobileMenuOpen = false)}
							>
								<div class="flex items-center gap-3">
									<item.icon class="h-5 w-5 " />
									<span>{item.label}</span>
								</div>
								<ChevronRight class="h-5 w-5" />
							</a>
						{/each}
					{/if}
					<!-- Mobile nav items -->
					{#each navItems as item}
						<a
							href={item.href}
							class="group relative flex items-center justify-between rounded-md px-3 py-2 transition-all hover:bg-primary/5 active:scale-[0.98]"
							onclick={() => (isMobileMenuOpen = false)}
						>
							<div class="flex items-center gap-3">
								<item.icon class="h-5 w-5 " />
								<span>{item.label}</span>
							</div>
							<ChevronRight class="h-5 w-5" />
						</a>
					{/each}

					<!-- Mobile auth section -->
					<div class="flex flex-col gap-3 pt-4">
						{#if !isAuthenticated}
							<Button
								variant="outline"
								class="w-full justify-center gap-2 px-3 py-2 transition-all hover:bg-primary/5 active:scale-[0.98]"
								href="/login"
							>
								Login
							</Button>
							<Button
								class="w-full justify-center gap-2 px-3 py-2 transition-all hover:bg-primary/90 active:scale-[0.98]"
								href="/register"
							>
								Register
							</Button>
						{:else}
							<Button
								variant="destructive"
								class="w-full justify-center"
								on:click={handleLogout}
								size="sm"
							>
								Logout
							</Button>
						{/if}
					</div>
				</div>
			</div>
		</div>
	{/if}
</nav>

<style>
	nav {
		background: linear-gradient(to bottom, rgba(255, 255, 255, 0.9), rgba(255, 255, 255, 0.8));
	}

	@media (max-width: 768px) {
		nav {
			position: fixed;
			width: 100%;
			top: 0;
			left: 0;
			z-index: 50;
			backdrop-filter: blur(8px);
		}
	}

	/* Smooth transition for dropdown */
	:global(.dropdown-content) {
		transition:
			transform 0.2s ease-in-out,
			opacity 0.2s ease-in-out;
	}
</style>
