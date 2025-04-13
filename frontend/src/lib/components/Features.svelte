<script lang="ts">
	import { Shield, FileKey, Lock, Layout } from 'lucide-svelte';
</script>

<section class="w-full px-4 py-16 md:px-6" id="features">
	<div class="mx-auto grid max-w-7xl gap-6 md:grid-cols-2">
		<!-- Watermark Protection -->
		<div class="feature-card">
			<Shield class="feature-icon" />
			<div class="feature-content">
				<h3 class="feature-title">Watermark Protection</h3>
				<p class="feature-description">
					Easily apply customizable watermarks to your images, ensuring unauthorized use is
					prevented.
				</p>
			</div>
		</div>

		<!-- Metadata Security -->
		<div class="feature-card">
			<FileKey class="feature-icon" />
			<div class="feature-content">
				<h3 class="feature-title">Metadata Security</h3>
				<p class="feature-description">
					Embed secure metadata in your images to track usage and ownership effortlessly.
				</p>
			</div>
		</div>

		<!-- Access Controls -->
		<div class="feature-card">
			<Lock class="feature-icon" />
			<div class="feature-content">
				<h3 class="feature-title">Access Controls</h3>
				<p class="feature-description">
					Manage who can view or use your images with advanced access control settings.
				</p>
			</div>
		</div>

		<!-- User-Friendly Interface -->
		<div class="feature-card">
			<Layout class="feature-icon" />
			<div class="feature-content">
				<h3 class="feature-title">User-Friendly Interface</h3>
				<p class="feature-description">
					Enjoy a seamless experience with our intuitive interface designed for all skill levels.
				</p>
			</div>
		</div>
	</div>
</section>

<style>
	.feature-card {
		display: flex;
		align-items: start;
		gap: 1.25rem;
		padding: 1.5rem;
		border-radius: 1rem;
		background-color: hsl(var(--background));
		border: 1px solid hsl(var(--border));
		transition: all 0.3s ease;
		position: relative;
		overflow: hidden;
	}

	.feature-card::before {
		content: '';
		position: absolute;
		top: 0;
		left: 0;
		right: 0;
		bottom: 0;
		background: linear-gradient(
			135deg,
			hsl(var(--primary) / 0.1) 0%,
			hsl(var(--primary) / 0.05) 100%
		);
		opacity: 0;
		transition: opacity 0.3s ease;
	}

	.feature-card:hover {
		transform: translateY(-2px);
		box-shadow: 0 10px 30px -10px hsl(var(--primary) / 0.2);
	}

	.feature-card:hover::before {
		opacity: 1;
	}

	.feature-icon {
		width: 2rem;
		height: 2rem;
		color: hsl(var(--primary));
		transition: transform 0.3s ease;
		flex-shrink: 0;
		position: relative;
		z-index: 1;
	}

	.feature-card:hover .feature-icon {
		transform: scale(1.1);
	}

	.feature-content {
		position: relative;
		z-index: 1;
	}

	.feature-title {
		font-size: 1.25rem;
		font-weight: 600;
		margin-bottom: 0.5rem;
		color: hsl(var(--foreground));
	}

	.feature-description {
		color: hsl(var(--muted-foreground));
		line-height: 1.6;
	}

	@media (max-width: 768px) {
		.feature-card {
			margin-bottom: 0.5rem;
		}
	}
</style>
