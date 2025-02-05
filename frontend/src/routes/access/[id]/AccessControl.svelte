<script>
	import { onMount, onDestroy } from 'svelte';
	import { Trash2, Plus, Link } from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Alert, AlertDescription } from '$lib/components/ui/alert';
	import * as Select from '$lib/components/ui/select';
	import { Tabs, TabsList, TabsTrigger, TabsContent } from '$lib/components/ui/tabs';
	import { toast } from 'svelte-sonner';
	import { Checkbox } from '$lib/components/ui/checkbox';
	import { Label } from '$lib/components/ui/label';

	export let imageUrl;
	export let imageId;

	const CONTAINER_WIDTH = 900;
	const CONTAINER_HEIGHT = 600;

	// Access control state
	let accessList = [];
	let isSaving = false;

	// New access form state
	let newAccess = {
		type: 'view',
		expirationDays: 7,
		allowDownload: false,
		allowSharing: false,
		maxViews: 0,
		password: ''
	};

	// Access type options
	const accessTypes = [
		{ value: 'view', label: 'View Only' },
		{ value: 'download', label: 'Download' },
		{ value: 'full', label: 'Full Access' }
	];

	// Expiration time options
	const expirationOptions = [
		{ value: 1, label: '24 Hours' },
		{ value: 7, label: '7 Days' },
		{ value: 30, label: '30 Days' },
		{ value: 365, label: '1 Year' },
		{ value: 0, label: 'Never' }
	];

	// Add this function to calculate image dimensions while maintaining aspect ratio
	function calculateImageDimensions(naturalWidth, naturalHeight) {
		const containerRatio = CONTAINER_WIDTH / CONTAINER_HEIGHT;
		const imageRatio = naturalWidth / naturalHeight;

		if (imageRatio > containerRatio) {
			// Image is wider than container ratio
			return {
				width: CONTAINER_WIDTH,
				height: CONTAINER_WIDTH / imageRatio
			};
		} else {
			// Image is taller than container ratio
			return {
				width: CONTAINER_HEIGHT * imageRatio,
				height: CONTAINER_HEIGHT
			};
		}
	}

	// Add state for image dimensions
	let imageDimensions = {
		width: 0,
		height: 0
	};

	// Handle image load
	function handleImageLoad(event) {
		const img = event.target;
		imageDimensions = calculateImageDimensions(img.naturalWidth, img.naturalHeight);
	}

	function addNewAccess() {
		const access = {
			...newAccess,
			id: Date.now(),
			created: new Date(),
			token: generateToken()
		};
		accessList = [...accessList, access];
		resetNewAccessForm();
		toast.success('New access created successfully');
	}

	function deleteAccess(id) {
		accessList = accessList.filter((access) => access.id !== id);
		toast.success('Access removed successfully');
	}

	function generateToken() {
		return Math.random().toString(36).substr(2, 9);
	}

	function resetNewAccessForm() {
		newAccess = {
			type: 'view',
			expirationDays: 7,
			allowDownload: false,
			allowSharing: false,
			maxViews: 0,
			password: ''
		};
	}

	function copyToken(token) {
		navigator.clipboard.writeText(token);
		toast.success('Token copied to clipboard');
	}

	async function saveAccessSettings() {
		try {
			isSaving = true;
			// Add API call here to save settings
			await new Promise((resolve) => setTimeout(resolve, 1000)); // Simulated API call
			toast.success('Access settings saved successfully');
		} catch (error) {
			toast.error('Failed to save access settings');
		} finally {
			isSaving = false;
		}
	}
</script>

<div class="mx-auto max-w-[1400px] p-6">
	<div class="grid gap-8 lg:grid-cols-[1.2fr,1fr]">
		<!-- Image Preview Card -->
		<Card class="h-fit">
			<CardHeader>
				<CardTitle>Image Preview</CardTitle>
			</CardHeader>
			<CardContent class="p-6">
				<div
					class="relative flex items-center justify-center overflow-hidden rounded-lg border bg-muted/50"
					style="min-height: {CONTAINER_HEIGHT}px;"
				>
					<img
						src={imageUrl}
						alt="Preview"
						on:load={handleImageLoad}
						class="max-h-[600px] w-auto object-contain"
					/>
				</div>
			</CardContent>
		</Card>

		<!-- Access Control Card -->
		<Card class="h-fit">
			<CardHeader>
				<CardTitle>Access Control</CardTitle>
			</CardHeader>
			<CardContent class="space-y-6">
				<Tabs defaultValue="basic" class="w-full">
					<TabsList class="grid w-full grid-cols-2">
						<TabsTrigger value="basic">Current Access</TabsTrigger>
						<TabsTrigger value="advanced">Create New Access</TabsTrigger>
					</TabsList>

					<TabsContent value="basic" class="space-y-4 pt-4">
						<div class="h-[400px] overflow-y-auto pr-2">
							<!-- Added fixed height container with scroll -->
							{#if accessList.length === 0}
								<Alert variant="default">
									<AlertDescription>No access tokens created yet.</AlertDescription>
								</Alert>
							{:else}
								<div class="space-y-3">
									{#each accessList as access}
										<Card>
											<CardContent class="p-4">
												<div class="flex items-start justify-between gap-4">
													<div class="space-y-2">
														<div>
															<h4 class="font-semibold">{access.type.toUpperCase()} Access</h4>
															<p class="text-sm text-muted-foreground">
																Expires: {access.expirationDays === 0
																	? 'Never'
																	: `in ${access.expirationDays} days`}
															</p>
														</div>
														<div class="flex items-center gap-2">
															<code class="rounded bg-muted px-2 py-1 text-sm">{access.token}</code>
															<Button
																variant="ghost"
																size="sm"
																on:click={() => copyToken(access.token)}
															>
																<Link class="h-4 w-4" />
															</Button>
														</div>
													</div>
													<Button
														variant="destructive"
														size="sm"
														on:click={() => deleteAccess(access.id)}
													>
														<Trash2 class="h-4 w-4" />
													</Button>
												</div>
											</CardContent>
										</Card>
									{/each}
								</div>
							{/if}
						</div></TabsContent
					>

					<TabsContent value="advanced" class="pt-4">
						<div class="h-[400px] overflow-y-auto pr-2">
							<!-- Added fixed height container with scroll -->
							<div class="space-y-4">
								<div class="grid gap-4 sm:grid-cols-2">
									<div class="space-y-2">
										<Label>Access Type</Label>
										<Select.Root bind:value={newAccess.type}>
											<Select.Trigger>
												<Select.Value placeholder="Select access type" />
											</Select.Trigger>
											<Select.Content>
												{#each accessTypes as type}
													<Select.Item value={type.value}>{type.label}</Select.Item>
												{/each}
											</Select.Content>
										</Select.Root>
									</div>

									<div class="space-y-2">
										<Label>Expiration Time</Label>
										<Select.Root bind:value={newAccess.expirationDays}>
											<Select.Trigger>
												<Select.Value placeholder="Select expiration time" />
											</Select.Trigger>
											<Select.Content>
												{#each expirationOptions as option}
													<Select.Item value={option.value}>{option.label}</Select.Item>
												{/each}
											</Select.Content>
										</Select.Root>
									</div>
								</div>

								<div class="space-y-3">
									<Label>Additional Options</Label>
									<div class="grid gap-2 sm:grid-cols-2">
										<div class="flex items-center space-x-2">
											<Checkbox id="allowDownload" bind:checked={newAccess.allowDownload} />
											<Label for="allowDownload">Allow Download</Label>
										</div>
										<div class="flex items-center space-x-2">
											<Checkbox id="allowSharing" bind:checked={newAccess.allowSharing} />
											<Label for="allowSharing">Allow Sharing</Label>
										</div>
									</div>
								</div>

								<div class="grid gap-4 sm:grid-cols-2">
									<div class="space-y-2">
										<Label>Max Views</Label>
										<Input
											type="number"
											min="0"
											bind:value={newAccess.maxViews}
											placeholder="0 for unlimited"
										/>
									</div>

									<div class="space-y-2">
										<Label>Password Protection</Label>
										<Input type="password" bind:value={newAccess.password} placeholder="Optional" />
									</div>
								</div>

								<Button class="w-full" on:click={addNewAccess}>
									<Plus class="mr-2 h-4 w-4" />
									Create New Access
								</Button>
							</div>
						</div></TabsContent
					>
				</Tabs>

				<div class="border-t pt-4">
					<!-- Added border and padding to separate the save button -->
					<Button
						class="w-full"
						variant="default"
						on:click={saveAccessSettings}
						disabled={isSaving}
					>
						{isSaving ? 'Saving Settings...' : 'Save All Settings'}
					</Button>
				</div>
			</CardContent>
		</Card>
	</div>
</div>

<style>
	/* Add these styles */
	:global(.card) {
		height: fit-content;
	}

	img {
		max-width: 100%;
		height: auto;
	}

	/* Add custom scrollbar styles */
	.overflow-y-auto {
		scrollbar-width: thin;
		scrollbar-color: var(--scrollbar) var(--scrollbar-bg);
	}

	.overflow-y-auto::-webkit-scrollbar {
		width: 8px;
	}

	.overflow-y-auto::-webkit-scrollbar-track {
		background: var(--scrollbar-bg);
		border-radius: 4px;
	}

	.overflow-y-auto::-webkit-scrollbar-thumb {
		background-color: var(--scrollbar);
		border-radius: 4px;
	}

	:global(:root) {
		--scrollbar: hsl(215.4 16.3% 56.9%);
		--scrollbar-bg: hsl(215.4 16.3% 46.9% / 0.1);
	}
</style>
