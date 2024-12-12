<script lang="js">
	import { Menu, Shield, X, ChevronRight, Album, DollarSign, Contact } from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';
	import { slide, fade } from 'svelte/transition';

	// Navigation items array with icons for better mobile experience
	const navItems = [
		{ label: 'Home', href: '#', icon: Shield },
		{ label: 'Gallery', href: '#', icon: Album },
		{ label: 'Pricing', href: '#', icon: DollarSign },
		{ label: 'Contact', href: '#', icon: Contact }
	];

	// Mobile menu state
	let isMobileMenuOpen = $state(false);

	/** Toggle mobile menu */
	const toggleMobileMenu = () => {
		isMobileMenuOpen = !isMobileMenuOpen;
	};
</script>

<!-- Navigation wrapper -->
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
				<span
					class="relative text-xl font-semibold after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 after:bg-primary after:transition-all after:duration-300 group-hover:after:w-full"
					>IGuardian</span
				>
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

			<!-- Auth buttons -->
			<div class="hidden items-center gap-2 md:flex">
				<Button
					variant="ghost"
					class="relative overflow-hidden px-3 transition-colors after:absolute after:bottom-0 after:left-0 after:h-[2px] after:w-0 after:bg-primary after:transition-all after:duration-300 hover:after:w-full"
					>Login</Button
				>
				<Button
					class="px-4 py-2 transition-transform duration-300 hover:scale-105 hover:shadow-lg hover:shadow-primary/20"
					>Register</Button
				>
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
					<!-- Mobile nav items -->
					{#each navItems as item}
						<a
							href={item.href}
							class="group relative flex items-center justify-between rounded-md px-3 py-2 text-muted-foreground transition-all hover:bg-primary/5 active:scale-[0.98]"
							onclick={() => (isMobileMenuOpen = false)}
						>
							<div class="flex items-center gap-3">
								<item.icon class="h-5 w-5 text-muted-foreground" />
								<span>{item.label}</span>
							</div>
							<ChevronRight class="h-5 w-5 text-muted-foreground" />
						</a>
					{/each}

					<!-- Mobile auth buttons -->
					<div class="flex flex-col gap-3 pt-4">
						<Button
							variant="outline"
							class="w-full justify-center gap-2 px-3 py-2 transition-all hover:bg-primary/5 active:scale-[0.98]"
						>
							Login
						</Button>
						<Button
							class="w-full justify-center gap-2 px-3 py-2 transition-all hover:bg-primary/90 active:scale-[0.98]"
						>
							Register
						</Button>
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
