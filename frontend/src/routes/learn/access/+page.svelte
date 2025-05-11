<script>
	import { Shield, Fingerprint } from 'lucide-svelte';
</script>

<div class="w-full bg-white text-gray-800 py-16 px-6 lg:px-24">
	<article class="max-w-screen-xl mx-auto space-y-16">
		<!-- Hero Header -->
		<header class="text-center">
			<div class="flex justify-center mb-4">
				<Shield class="h-10 w-10 text-primary" />
			</div>
			<h1 class="text-4xl sm:text-5xl font-extrabold mb-4">Access Controls: Secure Your Images</h1>
			<p class="text-xl text-gray-600 max-w-2xl mx-auto">
				Learn how to protect your images with granular access controls and user-specific permissions.
			</p>
		</header>

		<!-- What are Access Controls? -->
		<section class="grid md:grid-cols-2 gap-12 items-center">
			<div>
				<h2 class="text-2xl font-semibold mb-4">What are Access Controls?</h2>
				<p class="leading-relaxed">
					Access Controls are security measures that allow you to manage who can view, download, or modify your images. Think of it as a digital bouncer that checks credentials before allowing access to your protected content.
				</p>
			</div>
			<img src='/blog_imgs/access_control.png' alt="Access Control Example" class="rounded-lg shadow-md w-full" />
		</section>

		<!-- Key Features -->
		<section>
			<h2 class="text-2xl font-semibold mb-8 text-center">Key Features</h2>
			<div class="grid md:grid-cols-3 gap-8">
				<div class="border rounded-lg p-6 shadow-sm">
					<Shield class="h-6 w-6 text-primary mb-3" />
					<h3 class="text-lg font-semibold mb-2">User Management</h3>
					<p>Assign specific permissions to individual users or groups of users.</p>
				</div>
				<div class="border rounded-lg p-6 shadow-sm">
					<Shield class="h-6 w-6 text-primary mb-3" />
					<h3 class="text-lg font-semibold mb-2">Permission Levels</h3>
					<p>Set different access levels: view-only, download, or full editing rights.</p>
				</div>
				<div class="border rounded-lg p-6 shadow-sm">
					<Shield class="h-6 w-6 text-primary mb-3" />
					<h3 class="text-lg font-semibold mb-2">Visibility Control</h3>
					<p>Control who can see your images in search results and galleries.</p>
				</div>
			</div>
		</section>

		<!-- How It Works -->
		<section class="grid md:grid-cols-2 gap-12 items-center">
			<div>
				<h2 class="text-2xl font-semibold mb-4">How It Works</h2>
				<ol class="list-decimal space-y-4 pl-5">
					<li><strong>Set Up Access Rules:</strong> Define who can access your images and what they can do with them.</li>
					<li><strong>Invite Users:</strong> Send invitations to specific users or groups.</li>
					<li><strong>Monitor Access:</strong> Track who has accessed your images and when they were viewed.</li>
				</ol>
			</div>
			<img src="/blog_imgs/access_control_steps.png" class="rounded-lg shadow-md w-full" />
		</section>

		<!-- Best Practices -->
		<section>
			<h2 class="text-2xl font-semibold mb-6">Best Practices</h2>
			<ul class="list-disc pl-6 space-y-2">
				<li>Regularly review and update access permissions.</li>
				<li>Use the principle of least privilege - only grant necessary access.</li>
				<li>Set expiration dates for temporary access.</li>
				<li>Apply password protection for sensitive images.</li>
			</ul>
		</section>

		<!-- Common Use Cases -->
		<section>
			<h2 class="text-2xl font-semibold mb-6 text-center">Where It’s Used</h2>
			<div class="grid sm:grid-cols-2 md:grid-cols-3 gap-6 text-center">
				<div class="p-4 border rounded-lg">
					<h3 class="font-semibold text-lg">Client Galleries</h3>
					<p class="text-sm text-gray-600 mt-2">Share images with specific clients while keeping them private from others.</p>
				</div>
				<div class="p-4 border rounded-lg">
					<h3 class="font-semibold text-lg">Team Collaboration</h3>
					<p class="text-sm text-gray-600 mt-2">Allow team members to access and work on shared images.</p>
				</div>
				<div class="p-4 border rounded-lg">
					<h3 class="font-semibold text-lg">Limited Time Access</h3>
					<p class="text-sm text-gray-600 mt-2">Grant temporary access to images for specific events or projects.</p>
				</div>
			</div>
		</section>

	</article>
</div>
