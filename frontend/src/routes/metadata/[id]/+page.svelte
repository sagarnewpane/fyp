<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Tabs, TabsContent, TabsList, TabsTrigger } from '$lib/components/ui/tabs';
	import { Save, RefreshCcw, ImageIcon, Edit } from 'lucide-svelte';
	import { toast } from 'svelte-sonner';
	import { writable } from 'svelte/store';

	const imageId = $page.params.id;
	let loading = true;
	let error = null;

	// State for metadata
	let metadata = {};
	let editedMetadata = {};

	// Store to manage the expanded state of collapsible sections
	let expandedSections = writable({});

	function toggleSection(key) {
		expandedSections.update((state) => ({
			...state,
			[key]: !state[key]
		}));
	}

	// Load initial data from server
	onMount(async () => {
		try {
			const response = await fetch(`/api/metadata/${imageId}`);
			if (!response.ok) throw new Error('Failed to fetch metadata');
			const data = await response.json();
			metadata = data.metadata;
			// Initialize editedMetadata as a deep copy
			editedMetadata = JSON.parse(JSON.stringify(metadata));
		} catch (err) {
			console.error('Error loading metadata:', err);
			error = err.message;
			toast.error('Failed to load metadata');
		} finally {
			loading = false;
		}
	});

	// Update field value
	function updateField(category, section, field, value) {
		if (
			editedMetadata[category] &&
			editedMetadata[category][section] &&
			editedMetadata[category][section][field]
		) {
			editedMetadata[category][section][field].value = value;
		}
		editedMetadata = { ...editedMetadata };
	}

	// Save all changes
	async function saveMetadata() {
		try {
			loading = true;
			const updates = [];

			// Collect updates for all categories
			for (const [category, sections] of Object.entries(editedMetadata)) {
				for (const [section, fields] of Object.entries(sections)) {
					for (const [field, data] of Object.entries(fields)) {
						const originalValue = metadata[category]?.[section]?.[field]?.value;
						if (data.value !== originalValue) {
							updates.push({
								type: category.toLowerCase(),
								field_name: field,
								value: data.value
							});
						}
					}
				}
			}

			if (updates.length === 0) {
				toast.info('No changes to save');
				return;
			}

			const response = await fetch(`/api/metadata/${imageId}`, {
				method: 'PUT',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ updates })
			});

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.error || 'Failed to save changes');
			}

			// Update local state after successful save
			metadata = JSON.parse(JSON.stringify(editedMetadata));
			toast.success('Changes saved successfully');
		} catch (err) {
			console.error('Error saving metadata:', err);
			toast.error(err.message || 'Failed to save changes');
		} finally {
			loading = false;
		}
	}

	// Reset changes
	function resetMetadata() {
		editedMetadata = JSON.parse(JSON.stringify(metadata));
		toast.success('Changes reset');
	}

	// Computed: detect changes
	$: hasChanges = JSON.stringify(metadata) !== JSON.stringify(editedMetadata);
	// For tab iteration, we use all categories
	$: categories = Object.keys(metadata);
</script>

<div class="min-h-screen bg-background">
	{#if loading}
		<div class="flex min-h-screen items-center justify-center">
			<div class="animate-pulse text-muted-foreground">Loading metadata...</div>
		</div>
	{:else if error}
		<div class="flex min-h-screen items-center justify-center">
			<div class="text-destructive">{error}</div>
		</div>
	{:else}
		<header class="border-b bg-background px-6 py-3">
			<div class="mx-auto flex max-w-7xl items-center justify-between">
				<div class="space-y-1">
					<h1 class="text-2xl font-bold">Metadata Editor</h1>
					<p class="text-sm text-muted-foreground">
						View and edit image metadata
					</p>
				</div>
				<div class="flex gap-2">
					<Button variant="outline" on:click={resetMetadata} disabled={!hasChanges || loading}>
						<RefreshCcw class="mr-2 h-4 w-4" />
						Reset
					</Button>
					<Button on:click={saveMetadata} disabled={!hasChanges || loading}>
						{#if loading}
							<div
								class="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent"
							/>
							Saving...
						{:else}
							<Save class="mr-2 h-4 w-4" />
							Save Changes
						{/if}
					</Button>
				</div>
			</div>
		</header>

		<main class="p-6">
			<div class="mx-auto max-w-7xl space-y-6">
				<!-- Metadata Tabs -->
				<Tabs defaultValue="view" class="w-full">
					<TabsList class="grid w-full grid-cols-2 border-b border-border">
						<TabsTrigger
							value="view"
							class="data-[state=active]:border-b-2 data-[state=active]:border-primary"
						>
							<ImageIcon class="mr-2 h-4 w-4" />
							View Metadata
						</TabsTrigger>
						<TabsTrigger
							value="edit"
							class="data-[state=active]:border-b-2 data-[state=active]:border-primary"
						>
							<Edit class="mr-2 h-4 w-4" />
							Edit Metadata
						</TabsTrigger>
					</TabsList>

					<!-- View Tab -->
					<TabsContent value="view">
						<div class="space-y-6">
							{#each Object.entries(metadata) as [category, sections]}
								<div class="rounded-lg border bg-card shadow-sm">
									<div class="border-b bg-muted/50 px-4 py-3">
										<h2 class="font-semibold">{category}</h2>
									</div>
									<div class="divide-y">
										{#each Object.entries(sections) as [section, fields]}
											<div class="p-4">
												<h3 class="mb-3 font-medium text-muted-foreground">{section}</h3>
												<div class="ml-4 space-y-3">
													{#each Object.entries(fields) as [field, data]}
														<div class="flex items-start">
															<div class="w-1/3 text-sm font-medium text-muted-foreground">
																{data.label || field}:
															</div>
															<div class="w-2/3 text-sm">
																{data.value !== null ? data.value : '(No value)'}
															</div>
														</div>
													{/each}
												</div>
											</div>
										{/each}
									</div>
								</div>
							{/each}
						</div>
					</TabsContent>

					<!-- Edit Tab -->
					<TabsContent value="edit">
						<div class="space-y-6">
							{#each Object.entries(editedMetadata) as [category, sections]}
								<div class="rounded-lg border bg-card shadow-sm">
									<div class="border-b bg-muted/50 px-4 py-3">
										<h2 class="font-semibold">{category}</h2>
									</div>
									<div class="divide-y">
										{#each Object.entries(sections) as [section, fields]}
											<div class="p-4">
												<h3 class="mb-3 font-medium text-muted-foreground">{section}</h3>
												<div class="ml-4 space-y-3">
													{#each Object.entries(fields) as [field, data]}
														<div class="flex items-start">
															<div class="w-1/3 text-sm font-medium text-muted-foreground">
																{data.label || field}:
															</div>
															<div class="w-2/3">
																{#if data.type === 'textarea'}
																	<textarea
																		class="min-h-[100px] w-full rounded-md border bg-background p-2 text-sm"
																		value={data.value || ''}
																		placeholder={data.placeholder || 'Enter value'}
																		disabled={data.readonly || false}
																		on:input={(e) =>
																			updateField(category, section, field, e.target.value)}
																	/>
																{:else}
																	<Input
																		type={data.type === 'number' ? 'number' : 'text'}
																		value={data.value || ''}
																		placeholder={data.placeholder || 'Enter value'}
																		disabled={data.readonly || false}
																		step={data.step}
																		class="bg-background"
																		on:input={(e) =>
																			updateField(category, section, field, e.target.value)}
																	/>
																{/if}
															</div>
														</div>
													{/each}
												</div>
											</div>
										{/each}
									</div>
								</div>
							{/each}
						</div>
					</TabsContent>
				</Tabs>
			</div>
		</main>
	{/if}
</div>
