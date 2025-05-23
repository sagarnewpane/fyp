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
		{ text: 'Home', href: '/' },
		{ text: 'Blogs', href: '/blog' }
	];

	// Legal links
	const legalLinks = [
		{ text: 'Terms of Service', href: '/terms' },
		{ text: 'Privacy Policy', href: '/privacy' }
	];
</script>

<footer class="relative overflow-hidden bg-[#1A202C] px-4 py-16 text-[#A0AEC0]">
	<!-- Background Pattern - adjusted for dark navy -->
	<div class="absolute inset-0 opacity-5">
		<div
			class="absolute inset-0 bg-[radial-gradient(circle_500px_at_50%_200px,#2B6CB0,transparent)]"
		></div>
	</div>

	<div class="relative mx-auto max-w-7xl">
		<!-- Main Content -->
		<div class="mb-16 grid grid-cols-1 gap-12 md:grid-cols-2 lg:grid-cols-4">
			<!-- Company Info -->
			<div class="space-y-6">
				<div class="group flex items-center">
					<div class="flex h-8 w-8 items-center justify-center">
						<!-- LOGO  -->
						<img src="/crop.png" alt="Authograph Logo" />
					</div>
					<a href="/">
						<span class="relative text-xl font-semibold"> uthograph </span>
					</a>
				</div>
				<p class="text-sm leading-relaxed text-[#A0AEC0]">
					Protecting your visual assets before showing it publicly with advanced technology and
					industry-leading security measures.
				</p>
			</div>

			<!-- Quick Links -->
			<div class="space-y-6">
				<h3 class="text-lg font-semibold text-white">Quick Links</h3>
				<ul class="space-y-2">
					<!-- Changed from space-y-3 to space-y-2 for 8px spacing -->
					{#each quickLinks as link}
						<li>
							<a
								href={link.href}
								class="group flex items-center text-sm text-[#A0AEC0] transition-colors duration-200 hover:text-white"
							>
								<span
									class="mr-0 h-[2px] w-0 bg-[#2B6CB0] transition-all duration-200 group-hover:mr-2 group-hover:w-2"
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
				<ul class="space-y-2">
					<!-- Changed from space-y-3 to space-y-2 for 8px spacing -->
					{#each legalLinks as link}
						<li>
							<a
								href={link.href}
								class="group flex items-center text-sm text-[#A0AEC0] transition-colors duration-200 hover:text-white"
							>
								<span
									class="mr-0 h-[2px] w-0 bg-[#2B6CB0] transition-all duration-200 group-hover:mr-2 group-hover:w-2"
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
							class="text-[#A0AEC0] {hoverColor} transition-colors duration-300"
							aria-label={label}
						>
							<Icon size={24} />
						</a>
					{/each}
				</div>
			</div>
		</div>

		<!-- Divider -->
		<div
			class="h-px bg-gradient-to-r from-transparent via-[#A0AEC0] to-transparent opacity-20"
		></div>

		<!-- Copyright -->
		<div class="mt-8 text-center text-sm text-[#A0AEC0]">
			<p>© {currentYear} Authograph. All rights reserved.</p>
		</div>
	</div>
</footer>
