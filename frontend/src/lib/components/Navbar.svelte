<script lang="js">
	import { Menu, Shield, X, ChevronRight, Album, DollarSign, Contact } from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';
	import { slide, fade } from 'svelte/transition';
	import { authStore } from '$lib/stores/auth';
	import { goto, invalidate } from '$app/navigation';
	import {
		DropdownMenu,
		DropdownMenuTrigger,
		DropdownMenuContent,
		DropdownMenuItem
	} from '$lib/components/ui/dropdown-menu';
	import { Avatar, AvatarImage, AvatarFallback } from '$lib/components/ui/avatar';

	const user = $derived($authStore?.user || null);
	const isAuthenticated = $derived(Boolean($authStore?.isAuthenticated));

	let avatarUrl = null;
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

	const dropItems = [{ label: 'Profile', href: '/profile', icon: Shield }];

	let isMobileMenuOpen = $state(false);

	const toggleMobileMenu = () => {
		isMobileMenuOpen = !isMobileMenuOpen;
	};
</script>

<nav
	class="supports-[backdrop-filter]:bg-background/0.1 sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur"
>
	<div class="px-4">
		<div class="flex h-16 items-center justify-between">
			<!-- Logo and brand -->
			<div class="group flex items-center gap-2">
				<div
					class="flex h-8 w-8 items-center justify-center rounded-lg bg-primary transition-transform duration-300 group-hover:scale-110"
				>
					<Shield class="h-6 w-6 text-white" />
				</div>
				<a href="/">
					<span
						class="relative cursor-pointer text-xl font-semibold after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 after:bg-primary after:transition-all after:duration-300 group-hover:after:w-full"
						>IGuardian</span
					>
				</a>
			</div>

			<!-- Desktop navigation -->
			<div class="hidden md:flex md:items-center md:gap-4">
				{#each navItems as item}
					<a
						href={item.href}
						class="relative px-2 text-muted-foreground transition-colors after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 after:bg-primary after:transition-all after:duration-300 hover:text-foreground hover:after:w-full"
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
								<Avatar class="">
									{#if avatarUrl}
										<AvatarImage
											src={avatarUrl}
											alt="User avatar"
											on:error={() => {
												console.error('Failed to load avatar');
												avatarUrl = null;
											}}
										/>
									{/if}
									<AvatarFallback>
										{(user?.username && user.username[0].toUpperCase()) || '?'}
									</AvatarFallback>
								</Avatar>
							</DropdownMenuTrigger>
						</div>
						<DropdownMenuContent align="start" class=" place-items-center">
							{#each dropItems as item}
								<a href={item.href}>
									<DropdownMenuItem class="w-full cursor-pointer">{item.label}</DropdownMenuItem>
								</a>
							{/each}

							<DropdownMenuItem>
								<Button variant="destructive" class="w-full" on:click={handleLogout} size="sm">
									Logout
								</Button>
							</DropdownMenuItem>
						</DropdownMenuContent>
					</DropdownMenu>
				{:else}
					<Button
						variant="ghost"
						class="relative overflow-hidden px-3 transition-colors after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 after:bg-primary after:transition-all after:duration-300 hover:after:w-full"
						href="/login">Login</Button
					>
					<Button
						class="px-4 py-2 transition-transform duration-300 hover:scale-105 hover:shadow-lg hover:shadow-primary/20"
						href="/register">Register</Button
					>
				{/if}
			</div>

			<!-- Mobile menu button -->
			<Button
				variant="ghost"
				size="icon"
				on:click={toggleMobileMenu}
				class="relative after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 after:bg-primary after:transition-all after:duration-300 hover:after:w-full md:hidden"
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
									{(user?.username && user.username[0].toUpperCase()) || '?'}
								</AvatarFallback>
							</Avatar>
							<span class="text-xl font-semibold">
								{user.username
									? String(user.username).charAt(0).toUpperCase() + String(user.username).slice(1)
									: 'User'}
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
	/* Additional mobile-friendly styles */
	@media (max-width: 768px) {
		nav {
			position: fixed;
			width: 100%;
			top: 0;
			left: 0;
			z-index: 50;
		}
	}
</style>
