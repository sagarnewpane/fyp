<script>
	import { goto } from '$app/navigation';
	import { Trash2 } from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';
	import {
		Dialog,
		DialogContent,
		DialogHeader,
		DialogTitle,
		DialogDescription,
		DialogFooter
	} from '$lib/components/ui/dialog';
	// import { createEventDispatcher } from 'svelte';
	import { toast } from 'svelte-sonner';
	import { invalidateAll } from '$app/navigation';

	export let images = [];
	// const dispatch = createEventDispatcher();

	let deleteDialogOpen = false;
	let selectedImage = null;

	function openDeleteDialog(image, event) {
		event.preventDefault();
		event.stopPropagation();
		selectedImage = image;
		deleteDialogOpen = true;
	}

	async function handleDelete() {
		if (!selectedImage) return;

		try {
			const response = await fetch(`/api/images/${selectedImage.id}`, {
				method: 'DELETE',
				headers: {
					'Content-Type': 'application/json'
				}
			});

			if (response.ok) {
				deleteDialogOpen = false;
				// Update images locally instead of invalidating everything
				images = images.filter((img) => img.id !== selectedImage.id);
				selectedImage = null;
				toast.success('Image deleted successfully');
			} else {
				throw new Error('Failed to delete image');
			}
		} catch (error) {
			console.error('Error deleting image:', error);
			toast.error('Failed to delete image. Please try again.');
		}
	}
</script>

<!-- Delete Confirmation Dialog -->
<Dialog bind:open={deleteDialogOpen} onOpenChange={() => (selectedImage = null)}>
	<DialogContent class="sm:max-w-md">
		<DialogHeader>
			<DialogTitle>Delete Image</DialogTitle>
			<DialogDescription>
				Are you sure you want to delete "{selectedImage?.image_name}"? This action cannot be undone.
			</DialogDescription>
		</DialogHeader>
		<DialogFooter class="flex space-x-2 sm:justify-end">
			<Button
				variant="outline"
				on:click={() => {
					deleteDialogOpen = false;
					selectedImage = null;
				}}
			>
				Cancel
			</Button>
			<Button variant="destructive" on:click={handleDelete}>Delete</Button>
		</DialogFooter>
	</DialogContent>
</Dialog>

<section class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
	{#if images.length === 0}
		<div
			class="col-span-full flex min-h-[300px] items-center justify-center rounded-xl border-2 border-dashed border-gray-200 bg-gray-50"
		>
			<div class="text-center">
				<p class="mb-1 text-gray-500">No images available</p>
				<p class="text-sm text-gray-400">Try adjusting your filters</p>
			</div>
		</div>
	{:else}
		{#each images as image}
			<div class="group relative">
				<a
					href="images/{image.id}"
					class="block overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm transition-all duration-200 hover:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary"
				>
					<article class="relative">
						<div class="relative aspect-square overflow-hidden bg-gray-100">
							<img
								src={image.image_url}
								alt={image.image_name}
								class="h-full w-full object-cover transition-transform duration-300 ease-out group-hover:scale-105"
								loading="lazy"
							/>
						</div>

						<div
							class="absolute inset-0 flex items-end bg-gradient-to-t from-black/60 via-black/30 to-transparent opacity-0 transition-opacity duration-200 group-hover:opacity-100"
						>
							<div class="w-full p-4">
								<h3 class="truncate text-sm font-medium text-white">
									{image.image_name}
								</h3>
								<time datetime={image.created_at} class="mt-1 block text-xs text-white/90">
									{new Date(image.created_at).toLocaleDateString()}
								</time>
							</div>
						</div>
					</article>
				</a>
				<!-- Delete button -->
				<button
					class="absolute right-2 top-2 rounded-full bg-red-600 p-2 text-white opacity-0 transition-opacity duration-200 hover:bg-red-700 group-hover:opacity-100"
					on:click={(e) => openDeleteDialog(image, e)}
					title="Delete image"
				>
					<Trash2 class="h-4 w-4" />
				</button>
			</div>
		{/each}
	{/if}
</section>
