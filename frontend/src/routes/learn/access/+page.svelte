<script lang="ts">
	import { Shield, Users, Lock, Eye } from 'lucide-svelte';
</script>

<div class="container mx-auto max-w-4xl px-4 py-8">
	<header class="mb-8">
		<div class="mb-4 flex items-center gap-3">
			<Shield class="h-8 w-8 text-primary" />
			<h1 class="text-3xl font-bold">Access Controls</h1>
		</div>
		<p class="text-xl text-muted-foreground">
			Learn how to protect your images with granular access controls and user-specific permissions.
		</p>
	</header>

	<article class="prose prose-lg max-w-none">
		<section class="mb-8">
			<h2>What are Access Controls?</h2>
			<p>
				Access Controls are security measures that allow you to manage who can view, download, or modify your
				images. Think of it as a digital bouncer that checks credentials before allowing access to your
				protected content.
			</p>
		</section>

		<section class="mb-8">
			<h2>Key Features</h2>
			<div class="grid gap-6 md:grid-cols-2">
				<div class="rounded-lg border p-4">
					<Users class="mb-2 h-6 w-6 text-primary" />
					<h3 class="text-xl font-semibold">User Management</h3>
					<p>Assign specific permissions to individual users or groups of users.</p>
				</div>
				<div class="rounded-lg border p-4">
					<Lock class="mb-2 h-6 w-6 text-primary" />
					<h3 class="text-xl font-semibold">Permission Levels</h3>
					<p>Set different access levels: view-only, download, or full editing rights.</p>
				</div>
				<div class="rounded-lg border p-4">
					<Eye class="mb-2 h-6 w-6 text-primary" />
					<h3 class="text-xl font-semibold">Visibility Control</h3>
					<p>Control who can see your images in search results and galleries.</p>
				</div>
			</div>
		</section>

		<section class="mb-8">
			<h2>How It Works</h2>
			<ol class="list-decimal pl-6">
				<li class="mb-4">
					<strong>Set Up Access Rules</strong>
					<p>Define who can access your images and what they can do with them.</p>
				</li>
				<li class="mb-4">
					<strong>Invite Users</strong>
					<p>Send invitations to specific users or groups you want to grant access to.</p>
				</li>
				<li class="mb-4">
					<strong>Monitor Access</strong>
					<p>Track who has accessed your images and when they were viewed.</p>
				</li>
			</ol>
		</section>

		<section class="mb-8">
			<h2>Best Practices</h2>
			<ul class="list-disc pl-6">
				<li>Regularly review and update access permissions</li>
				<li>Use the principle of least privilege - only grant necessary access</li>
				<li>Keep track of who has access to sensitive images</li>
				<li>Set expiration dates for temporary access</li>
			</ul>
		</section>

		<section class="mb-8">
			<h2>Common Use Cases</h2>
			<div class="grid gap-4">
				<div class="rounded-lg border p-4">
					<h3 class="text-xl font-semibold">Client Galleries</h3>
					<p>Share images with specific clients while keeping them private from others.</p>
				</div>
				<div class="rounded-lg border p-4">
					<h3 class="text-xl font-semibold">Team Collaboration</h3>
					<p>Allow team members to access and work on shared images with appropriate permissions.</p>
				</div>
				<div class="rounded-lg border p-4">
					<h3 class="text-xl font-semibold">Limited Time Access</h3>
					<p>Grant temporary access to images for specific events or projects.</p>
				</div>
			</div>
		</section>
	</article>
</div> 