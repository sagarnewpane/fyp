<script>
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Tabs, TabsContent, TabsList, TabsTrigger } from '$lib/components/ui/tabs';
	import {
		Dialog,
		DialogContent,
		DialogDescription,
		DialogHeader,
		DialogTitle,
		DialogTrigger,
		DialogFooter
	} from '$lib/components/ui/dialog';
	import { Plus, Save, RefreshCcw, ImageIcon, Edit, X } from 'lucide-svelte';
	import { toast } from 'svelte-sonner';
	import { writable } from 'svelte/store';

	const imageId = $page.params.id;
	let loading = true;
	let error = null;
	let showAddCustomDialog = true;

	// State for metadata
	let metadata = {};
	let editedMetadata = {};

	// State for new custom metadata
	let newCustomTag = {
		name: '',
		value: ''
	};

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
			// Ensure custom key exists
			if (!editedMetadata.custom) {
				editedMetadata.custom = {};
			}
			if (!metadata.custom) {
				metadata.custom = {};
			}
		} catch (err) {
			console.error('Error loading metadata:', err);
			error = err.message;
			toast.error('Failed to load metadata');
		} finally {
			loading = false;
		}
	});

	// Function to add custom metadata
	async function addCustomMetadata(event) {
		try {
			if (!newCustomTag.name || !newCustomTag.value) {
				toast.error('Name and value are required');
				return;
			}

			const response = await fetch(`/api/metadata/${imageId}/custom`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					tag_name: newCustomTag.name,
					value: newCustomTag.value
				})
			});

			if (!response.ok) {
				const errorData = await response.json();
				throw new Error(errorData.error || 'Failed to add custom metadata');
			}

			const newField = await response.json();

			// Update local state
			metadata.custom = {
				...metadata.custom,
				[newField.tag_name]: {
					value: newField.value,
					type: 'string',
					label: newField.tag_name
				}
			};
			editedMetadata.custom = { ...metadata.custom };

			// Reset form
			newCustomTag = { name: '', value: '' };
			toast.success('Custom metadata added');
		} catch (err) {
			console.error('Error adding custom metadata:', err);
			toast.error(err.message || 'Failed to add custom metadata');
		}
	}

	// Delete custom metadata
	// Function to delete custom metadata
	async function deleteCustomMetadata(tagName) {
		try {
			const response = await fetch(
				`/api/metadata/${imageId}?type=custom&field=${encodeURIComponent(tagName)}`,
				{
					method: 'DELETE'
				}
			);

			if (!response.ok) throw new Error('Failed to delete custom metadata');

			// Update local state
			const { [tagName]: removed, ...rest } = metadata.custom;
			metadata.custom = rest;
			editedMetadata.custom = { ...rest };

			toast.success('Custom metadata deleted');
		} catch (err) {
			console.error('Error deleting custom metadata:', err);
			toast.error('Failed to delete custom metadata');
		}
	}

	// Update field value
	function updateField(category, section, field, value) {
		if (
			editedMetadata[category] &&
			editedMetadata[category][section] &&
			editedMetadata[category][section][field]
		) {
			editedMetadata[category][section][field].value = value;
		} else if (category === 'custom' && editedMetadata.custom[field]) {
			editedMetadata.custom[field].value = value;
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
				if (category !== 'custom') {
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
			}

			// Collect custom updates
			for (const [field, data] of Object.entries(editedMetadata.custom)) {
				const originalValue = metadata.custom[field]?.value;
				if (data.value !== originalValue) {
					updates.push({
						type: 'custom',
						field_name: field,
						value: data.value
					});
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

	console.log(metadata);

	// Computed: detect changes
	$: hasChanges = JSON.stringify(metadata) !== JSON.stringify(editedMetadata);
	$: console.log(metadata);
	// For tab iteration, we use all categories except custom
	$: categories = Object.keys(metadata).filter((key) => key !== 'custom');
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
		<header class="border-b px-6 py-3">
			<div class="mx-auto flex max-w-7xl items-center justify-between">
				<h1 class="text-xl font-semibold">Metadata Editor</h1>
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
				<!-- Add Custom Metadata Dialog -->
				<Dialog>
					<DialogTrigger>
						<Button variant="outline">
							<Plus class="mr-2 h-4 w-4" />
							Add Custom Metadata
						</Button>
					</DialogTrigger>

					<DialogContent>
						<DialogHeader>
							<DialogTitle>Add Custom Metadata</DialogTitle>
							<DialogDescription>Add a new custom metadata field to your image.</DialogDescription>
						</DialogHeader>

						<form on:submit|preventDefault={addCustomMetadata} class="grid gap-4 py-4">
							<div class="grid gap-2">
								<label for="tagName" class="text-sm font-medium">Field Name</label>
								<Input
									id="tagName"
									bind:value={newCustomTag.name}
									placeholder="Enter field name"
									required
								/>
							</div>
							<div class="grid gap-2">
								<label for="tagValue" class="text-sm font-medium">Value</label>
								<Input
									id="tagValue"
									bind:value={newCustomTag.value}
									placeholder="Enter value"
									required
								/>
							</div>
							<DialogFooter>
								<Button type="submit">Add Field</Button>
							</DialogFooter>
						</form>
					</DialogContent>
				</Dialog>

				<!-- Metadata Tabs -->
				<Tabs defaultValue="view" class="w-full">
					<TabsList class="grid w-full grid-cols-2">
						<TabsTrigger value="view">
							<ImageIcon class="mr-2 h-4 w-4" />
							View Metadata
						</TabsTrigger>
						<TabsTrigger value="edit">
							<Edit class="mr-2 h-4 w-4" />
							Edit Metadata
						</TabsTrigger>
					</TabsList>

					<!-- View Tab -->
					<TabsContent value="view">
						<div class="space-y-6">
							{#each Object.entries(metadata) as [category, sections]}
								{#if category !== 'custom'}
									<div class="rounded-md border bg-card">
										<div class="border-b px-4 py-3">
											<h2 class="font-semibold">{category}</h2>
										</div>
										<div class="divide-y">
											{#each Object.entries(sections) as [section, fields]}
												<div class="p-4">
													<h3 class="font-medium">{section}</h3>
													<div class="ml-4">
														{#each Object.entries(fields) as [field, data]}
															<div class="border-b py-2 last:border-b-0">
																<div class="flex items-start">
																	<div class="w-1/3 text-sm font-medium text-muted-foreground">
																		{data.label || field}:
																	</div>
																	<div class="w-2/3 text-sm">
																		{data.value !== null ? data.value : '(No value)'}
																	</div>
																</div>
															</div>
														{/each}
													</div>
												</div>
											{/each}
										</div>
									</div>
								{/if}
							{/each}

							<!-- Custom Metadata -->
							{#if Object.keys(metadata.custom).length > 0}
								<div class="rounded-md border bg-card">
									<div class="border-b px-4 py-3">
										<h2 class="font-semibold">Custom Metadata</h2>
									</div>
									<div class="divide-y">
										{#each Object.entries(metadata.custom) as [field, data]}
											<div class="flex p-4 hover:bg-muted/50">
												<div class="w-1/3">
													<div class="flex items-center justify-between">
														<p class="font-medium">{data.label || field}</p>
														<Button
															variant="ghost"
															size="sm"
															class="h-8 w-8 p-0"
															on:click={() => deleteCustomMetadata(field)}
														>
															<X class="h-4 w-4" />
														</Button>
													</div>
													<p class="mt-1 text-sm text-muted-foreground">Custom field</p>
													<p class="mt-1 text-xs text-muted-foreground">
														Type: {data.type || 'string'}
													</p>
												</div>
												<div class="w-2/3">
													<div class="text-sm">{data.value || '(No value)'}</div>
												</div>
											</div>
										{/each}
									</div>
								</div>
							{/if}
						</div>
					</TabsContent>

					<!-- Edit Tab -->
					<TabsContent value="edit">
						<div class="space-y-6">
							{#each Object.entries(editedMetadata) as [category, sections]}
								{#if category !== 'custom'}
									<div class="rounded-md border bg-card">
										<div class="border-b px-4 py-3">
											<h2 class="font-semibold">{category}</h2>
										</div>
										<div class="divide-y">
											{#each Object.entries(sections) as [section, fields]}
												<div class="p-4">
													<h3 class="font-medium">{section}</h3>
													<div class="ml-4">
														{#each Object.entries(fields) as [field, data]}
															<div class="border-b py-2 last:border-b-0">
																<div class="flex items-start">
																	<div class="w-1/3 text-sm font-medium text-muted-foreground">
																		{data.label || field}:
																	</div>
																	<div class="w-2/3">
																		{#if data.type === 'textarea'}
																			<textarea
																				class="min-h-[100px] w-full rounded border p-2"
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
																				on:input={(e) =>
																					updateField(category, section, field, e.target.value)}
																			/>
																		{/if}
																	</div>
																</div>
															</div>
														{/each}
													</div>
												</div>
											{/each}
										</div>
									</div>
								{/if}
							{/each}

							<!-- Custom Metadata Edit -->
							{#if Object.keys(editedMetadata.custom).length > 0}
								<div class="rounded-md border bg-card">
									<div class="border-b px-4 py-3">
										<h2 class="font-semibold">Custom Metadata</h2>
									</div>
									<div class="divide-y">
										{#each Object.entries(editedMetadata.custom) as [field, data]}
											<div class="flex p-4 hover:bg-muted/50">
												<div class="w-1/3">
													<div class="flex items-center justify-between">
														<p class="font-medium">{data.label || field}</p>
														<Button
															variant="ghost"
															size="sm"
															class="h-8 w-8 p-0"
															on:click={() => deleteCustomMetadata(field)}
														>
															<X class="h-4 w-4" />
														</Button>
													</div>
													<p class="mt-1 text-sm text-muted-foreground">Custom field</p>
													<p class="mt-1 text-xs text-muted-foreground">
														Type: {data.type || 'string'}
													</p>
												</div>
												<div class="w-2/3">
													<Input
														value={data.value || ''}
														placeholder="Enter value"
														on:input={(e) => updateField('custom', '', field, e.target.value)}
													/>
												</div>
											</div>
										{/each}
									</div>
								</div>
							{/if}
						</div>
					</TabsContent>
				</Tabs>
			</div>
		</main>
	{/if}
</div>
