<script lang="ts">
	import { Shield, FileKey, Lock, Layout } from 'lucide-svelte';
</script>

<section class="w-full px-4 md:px-6" id="features">
	<div class="mx-auto grid max-w-7xl gap-8 md:grid-cols-2">
		<!-- Watermark Protection -->
		<div class="flex items-start gap-4">
			<Shield class="h-8 w-8 text-primary" />
			<div class="flex flex-col gap-2">
				<h3 class="text-xl font-semibold">Watermark Protection</h3>
				<p class="text-muted-foreground">
					Easily apply customizable watermarks to your images, ensuring unauthorized use is
					prevented.
				</p>
			</div>
		</div>

		<!-- Metadata Security -->
		<div class="flex items-start gap-4">
			<FileKey class="h-8 w-8 text-primary" />
			<div class="flex flex-col gap-2">
				<h3 class="text-xl font-semibold">Metadata Security</h3>
				<p class="text-muted-foreground">
					Embed secure metadata in your images to track usage and ownership effortlessly.
				</p>
			</div>
		</div>

		<!-- Access Controls -->
		<div class="flex items-start gap-4">
			<Lock class="h-8 w-8 text-primary" />
			<div class="flex flex-col gap-2">
				<h3 class="text-xl font-semibold">Access Controls</h3>
				<p class="text-muted-foreground">
					Manage who can view or use your images with advanced access control settings.
				</p>
			</div>
		</div>

		<!-- User-Friendly Interface -->
		<div class="flex items-start gap-4">
			<Layout class="h-8 w-8 text-primary" />
			<div class="flex flex-col gap-2">
				<h3 class="text-xl font-semibold">User-Friendly Interface</h3>
				<p class="text-muted-foreground">
					Enjoy a seamless experience with our intuitive interface designed for all skill levels.
				</p>
			</div>
		</div>
	</div>
</section>
