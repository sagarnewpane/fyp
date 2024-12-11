<script>
	import { Facebook, Twitter, Instagram, Linkedin, Shield } from 'lucide-svelte';

	// Current year for copyright
	const currentYear = new Date().getFullYear();

	// Social media links with hover colors
	const socialLinks = [
		{
			icon: Facebook,
			href: 'https://facebook.com',
			label: 'Facebook',
			hoverColor: 'hover:text-blue-500'
		},
		{
			icon: Twitter,
			href: 'https://twitter.com',
			label: 'Twitter',
			hoverColor: 'hover:text-sky-500'
		},
		{
			icon: Instagram,
			href: 'https://instagram.com',
			label: 'Instagram',
			hoverColor: 'hover:text-pink-500'
		},
		{
			icon: Linkedin,
			href: 'https://linkedin.com',
			label: 'LinkedIn',
			hoverColor: 'hover:text-blue-600'
		}
	];

	// Quick links
	const quickLinks = [
		{ text: 'Home', href: '#home' },
		{ text: 'Features', href: '#features' },
		{ text: 'Contact', href: '#contact' }
	];

	// Legal links
	const legalLinks = [
		{ text: 'Terms of Service', href: '#terms' },
		{ text: 'Privacy Policy', href: '#privacy' },
		{ text: 'Cookie Policy', href: '#cookies' }
	];
</script>

<footer
	class="relative overflow-hidden bg-gradient-to-br from-zinc-900 to-zinc-950 px-4 py-16 text-zinc-300"
>
	<!-- Background Pattern -->
	<div class="absolute inset-0 opacity-5">
		<div
			class="absolute inset-0 bg-[radial-gradient(circle_500px_at_50%_200px,#3b82f6,transparent)]"
		></div>
	</div>

	<div class="relative mx-auto max-w-7xl">
		<!-- Main Content -->
		<div class="mb-16 grid grid-cols-1 gap-12 md:grid-cols-2 lg:grid-cols-4">
			<!-- Company Info -->
			<div class="space-y-6">
				<div class="flex items-center space-x-2">
					<Shield class="text-muted-foreground h-5 w-5" />
					<h2
						class="bg-gradient-to-r from-white to-zinc-400 bg-clip-text text-2xl font-bold text-transparent"
					>
						ImageGuard
					</h2>
				</div>
				<p class="text-sm leading-relaxed text-zinc-400">
					Protecting your visual assets with advanced technology and industry-leading security
					measures.
				</p>
			</div>

			<!-- Quick Links -->
			<div class="space-y-6">
				<h3 class="text-lg font-semibold text-white">Quick Links</h3>
				<ul class="space-y-3">
					{#each quickLinks as link}
						<li>
							<a
								href={link.href}
								class="group flex items-center text-sm text-zinc-400 transition-colors duration-300 hover:text-white"
							>
								<span
									class="mr-0 h-[2px] w-0 bg-blue-500 transition-all duration-300 group-hover:mr-2 group-hover:w-2"
								></span>
								{link.text}
							</a>
						</li>
					{/each}
				</ul>
			</div>

			<!-- Legal -->
			<div class="space-y-6">
				<h3 class="text-lg font-semibold text-white">Legal</h3>
				<ul class="space-y-3">
					{#each legalLinks as link}
						<li>
							<a
								href={link.href}
								class="group flex items-center text-sm text-zinc-400 transition-colors duration-300 hover:text-white"
							>
								<span
									class="mr-0 h-[2px] w-0 bg-blue-500 transition-all duration-300 group-hover:mr-2 group-hover:w-2"
								></span>
								{link.text}
							</a>
						</li>
					{/each}
				</ul>
			</div>

			<!-- Social Media -->
			<div class="space-y-6">
				<h3 class="text-lg font-semibold text-white">Connect</h3>
				<div class="flex space-x-5">
					{#each socialLinks as { icon: Icon, href, label, hoverColor }}
						<a
							{href}
							target="_blank"
							rel="noopener noreferrer"
							class="text-zinc-400 {hoverColor} transition-colors duration-300"
							aria-label={label}
						>
							<Icon size={24} />
						</a>
					{/each}
				</div>
			</div>
		</div>

		<!-- Divider -->
		<div class="h-px bg-gradient-to-r from-transparent via-zinc-700 to-transparent"></div>

		<!-- Copyright -->
		<div class="mt-8 text-center text-sm text-zinc-500">
			<p>© {currentYear} ImageGuard. All rights reserved.</p>
		</div>
	</div>
</footer>
