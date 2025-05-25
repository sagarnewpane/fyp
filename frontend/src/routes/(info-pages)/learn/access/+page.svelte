<script>
	import { Shield, Fingerprint } from 'lucide-svelte';
</script>

<div class="w-full bg-white px-6 py-16 text-gray-800 lg:px-24">
	<article class="mx-auto max-w-screen-xl space-y-16">
		<!-- Hero Header -->
		<header class="text-center">
			<div class="mb-4 flex justify-center">
				<Shield class="h-10 w-10 text-primary" />
			</div>
			<h1 class="mb-4 text-4xl font-extrabold sm:text-5xl">Access Controls: Secure Your Images</h1>
			<p class="mx-auto max-w-2xl text-xl text-gray-600">
				Learn how to protect your images with granular access controls and user-specific
				permissions.
			</p>
		</header>

		<!-- What are Access Controls? -->
		<section class="grid items-center gap-12 md:grid-cols-2">
			<div>
				<h2 class="mb-4 text-2xl font-semibold">What are Access Controls?</h2>
				<p class="leading-relaxed">
					Access Controls are security measures that allow you to manage who can view, download, or
					modify your images. Think of it as a digital bouncer that checks credentials before
					allowing access to your protected content.
				</p>
			</div>
			<img
				src="/blog_imgs/access.png"
				alt="Access Control Example"
				class="w-full rounded-lg shadow-md"
			/>
		</section>

		<!-- Key Features -->
		<section>
			<h2 class="mb-8 text-center text-2xl font-semibold">Key Features</h2>
			<div class="grid gap-8 md:grid-cols-3">
				<div class="rounded-lg border p-6 shadow-sm">
					<Shield class="mb-3 h-6 w-6 text-primary" />
					<h3 class="mb-2 text-lg font-semibold">User Management</h3>
					<p>Assign specific permissions to individual users or groups of users.</p>
				</div>
				<div class="rounded-lg border p-6 shadow-sm">
					<Shield class="mb-3 h-6 w-6 text-primary" />
					<h3 class="mb-2 text-lg font-semibold">Permission Levels</h3>
					<p>Set different access levels: view-only, download, or full editing rights.</p>
				</div>
				<div class="rounded-lg border p-6 shadow-sm">
					<Shield class="mb-3 h-6 w-6 text-primary" />
					<h3 class="mb-2 text-lg font-semibold">Visibility Control</h3>
					<p>Control who can see your images in search results and galleries.</p>
				</div>
			</div>
		</section>

		<!-- How It Works -->
		<section class="grid items-center gap-12 md:grid-cols-2">
			<div>
				<h2 class="mb-4 text-2xl font-semibold">How It Works</h2>
				<ol class="list-decimal space-y-4 pl-5">
					<li>
						<strong>Set Up Access Rules:</strong> Define who can access your images and what they can
						do with them.
					</li>
					<li><strong>Invite Users:</strong> Send invitations to specific users or groups.</li>
					<li>
						<strong>Monitor Access:</strong> Track who has accessed your images and when they were viewed.
					</li>
				</ol>
			</div>
			<img src="/blog_imgs/access-control-steps.png" class="w-full rounded-lg shadow-md" />
		</section>

		<!-- Best Practices -->
		<section>
			<h2 class="mb-6 text-2xl font-semibold">Best Practices</h2>
			<ul class="list-disc space-y-2 pl-6">
				<li>Regularly review and update access permissions.</li>
				<li>Use the principle of least privilege - only grant necessary access.</li>
				<li>Set expiration dates for temporary access.</li>
				<li>Apply password protection for sensitive images.</li>
			</ul>
		</section>

		<!-- Common Use Cases -->
		<section>
			<h2 class="mb-6 text-center text-2xl font-semibold">Where It’s Used</h2>
			<div class="grid gap-6 text-center sm:grid-cols-2 md:grid-cols-3">
				<div class="rounded-lg border p-4">
					<h3 class="text-lg font-semibold">Client Galleries</h3>
					<p class="mt-2 text-sm text-gray-600">
						Share images with specific clients while keeping them private from others.
					</p>
				</div>
				<div class="rounded-lg border p-4">
					<h3 class="text-lg font-semibold">Team Collaboration</h3>
					<p class="mt-2 text-sm text-gray-600">
						Allow team members to access and work on shared images.
					</p>
				</div>
				<div class="rounded-lg border p-4">
					<h3 class="text-lg font-semibold">Limited Time Access</h3>
					<p class="mt-2 text-sm text-gray-600">
						Grant temporary access to images for specific events or projects.
					</p>
				</div>
			</div>
		</section>
	</article>
</div>
