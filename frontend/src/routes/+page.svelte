<script>
	import Hero from '$lib/components/Hero.svelte';
	import Features from '$lib/components/Features.svelte';
	import Gallery from '$lib/components/Gallery.svelte';
	import FAQ from '$lib/components/FAQ.svelte';
	import CTA from '$lib/components/CTA.svelte';
	import AccessRequests from '$lib/components/AccessRequests.svelte';
	import ActivityLogs from '$lib/components/ActivityLogs.svelte';
	import ImageGrid from '$lib/components/ImageGrid.svelte';
	import { authStore } from '$lib/stores/auth';

	$: isAuthenticated = Boolean($authStore?.isAuthenticated);
	export let data;
</script>

{#if !isAuthenticated}
	<main class="min-h-screen w-full bg-background text-foreground">
		<!-- Main sections with reduced gap -->
		<div class="flex flex-col gap-16">
			<Hero />
			<Features />
			<Gallery />
			<FAQ />
			<CTA />
		</div>
	</main>
{:else}
	<div class="min-h-screen w-full bg-background">
		<!-- Main Content -->
		<main class="mx-auto space-y-8 p-6">
			<!-- Activity and Requests Grid -->
			<div class="grid gap-6 lg:grid-cols-3">
				<div class="lg:col-span-2">
					<ActivityLogs />
				</div>
				<div class="lg:col-span-1">
					<AccessRequests />
				</div>
			</div>

			<div>
				<p class="pb-3 text-lg font-semibold">Recent Uploads</p>
				<ImageGrid images={data.images} />
			</div>
		</main>
	</div>
{/if}
