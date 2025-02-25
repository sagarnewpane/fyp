<script>
	import { onMount } from 'svelte';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Alert, AlertDescription, AlertTitle } from '$lib/components/ui/alert';
	import * as Select from '$lib/components/ui/select';
	import { Tabs, TabsList, TabsTrigger, TabsContent } from '$lib/components/ui/tabs';
	import { Badge } from '$lib/components/ui/badge';
	import { Checkbox } from '$lib/components/ui/checkbox';
	import { Label } from '$lib/components/ui/label';
	import { toast } from 'svelte-sonner';
	import ImagePreview from './ImagePreview.svelte';
	import {
		Trash2,
		Plus,
		Link,
		Mail,
		X,
		Download,
		Share2,
		Clock,
		Shield,
		Eye,
		SpellCheck,
		Database,
		Brain
	} from 'lucide-svelte';

	// Props
	export let imageUrl;
	export let imageId;
	export let imageSecurity;

	// State
	let activeAccessRules = [];
	let isSaving = false;
	let isLoading = false;
	let newAccess = {
		allowed_emails: [],
		requires_password: false,
		password: '',
		allow_download: false,
		max_views: 0,
		emailInput: '',
		protection_features: {
			watermark: false,
			hidden_watermark: false,
			metadata: false,
			ai_protection: false
		}
	};

	// Computed property for protection availability
	$: protectionStatus = {
		watermark: {
			available: imageSecurity?.watermark || false,
			title: 'Apply Watermark',
			description: 'Add visible watermark to protect from unauthorized sharing',
			icon: SpellCheck
		},
		hidden_watermark: {
			available: imageSecurity?.hidden_watermark || false,
			title: 'Apply Invisible Watermark',
			description: 'Embed hidden watermark for tracking source',
			icon: Shield
		},
		metadata: {
			available: imageSecurity?.metadata || false,
			title: 'Metadata Protection',
			description: 'Strip or modify sensitive metadata',
			icon: Database
		},
		ai_protection: {
			available: imageSecurity?.ai_protection || false,
			title: 'AI Protection',
			description: 'Apply AI-based protection against model training',
			icon: Brain
		}
	};

	// Fetch access rules function
	async function fetchAccessRules() {
		try {
			isLoading = true;
			const response = await fetch(`/api/images/${imageId}/access/`);
			if (response.ok) {
				const data = await response.json();
				activeAccessRules = data.rules;
			}
		} catch (error) {
			console.error('Error fetching access rules:', error);
			toast.error('Failed to fetch access rules');
		} finally {
			isLoading = false;
		}
	}

	onMount(() => {
		fetchAccessRules();
	});

	function isValidEmail(email) {
		return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
	}

	function addEmail() {
		if (newAccess.emailInput && isValidEmail(newAccess.emailInput)) {
			if (!newAccess.allowed_emails.includes(newAccess.emailInput)) {
				newAccess.allowed_emails = [...newAccess.allowed_emails, newAccess.emailInput];
				newAccess.emailInput = '';
			} else {
				toast.error('Email already added');
			}
		} else {
			toast.error('Please enter a valid email');
		}
	}

	function removeEmail(email) {
		newAccess.allowed_emails = newAccess.allowed_emails.filter((e) => e !== email);
	}

	async function createAccessRule() {
		try {
			isSaving = true;
			const accessData = {
				...newAccess,
				protection_features: {
					watermark: newAccess.protection_features.watermark,
					hidden_watermark: newAccess.protection_features.hidden_watermark,
					metadata: newAccess.protection_features.metadata,
					ai_protection: newAccess.protection_features.ai_protection // Added missing features
				}
			};

			const response = await fetch(`/api/images/${imageId}/access/`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(accessData)
			});

			if (!response.ok) {
				throw new Error('Failed to create access rule');
			}

			await fetchAccessRules();
			resetForm();
			toast.success('Access rule created successfully');
		} catch (error) {
			toast.error('Error creating access rule');
			console.error('Error:', error);
		} finally {
			isSaving = false;
		}
	}

	async function deleteAccessRule(ruleId) {
		try {
			const response = await fetch(`/api/images/${imageId}/access/${ruleId}`, {
				method: 'DELETE'
			});

			if (!response.ok) {
				throw new Error('Failed to delete access rule');
			}

			await fetchAccessRules();
			toast.success('Access rule deleted successfully');
		} catch (error) {
			toast.error('Error deleting access rule');
			console.error('Error:', error);
		}
	}

	function resetForm() {
		newAccess = {
			allowed_emails: [],
			requires_password: false,
			password: '',
			allow_download: false,
			max_views: 0,
			emailInput: '',
			protection_features: {
				watermark: false,
				hidden_watermark: false,
				metadata: false,
				ai_protection: false // Added missing features
			}
		};
	}

	function copyAccessLink(token) {
		const link = `${window.location.origin}/share/${token}`;
		navigator.clipboard.writeText(link);
		toast.success('Access link copied to clipboard');
	}
</script>

<div class="mx-auto max-w-7xl p-4 md:p-6 lg:p-8">
	<div class="grid gap-6 lg:grid-cols-[1.2fr,1fr]">
		<!-- Image Preview -->
		<ImagePreview {imageUrl}>
			<div class="space-y-2">
				<h3 class="font-semibold text-foreground">Image Information</h3>
				<div class="flex items-center gap-2 text-sm text-muted-foreground">
					<span>ID: {imageId}</span>
					<span>•</span>
					<span>{activeAccessRules.length} Active Access Rules</span>
				</div>
			</div>
		</ImagePreview>

		<!-- Access Control Panel -->
		<Card>
			<CardHeader>
				<CardTitle>Access Control</CardTitle>
			</CardHeader>
			<CardContent>
				<Tabs defaultValue="current">
					<TabsList class="grid w-full grid-cols-2">
						<TabsTrigger value="current">Active Rules</TabsTrigger>
						<TabsTrigger value="new">Create New</TabsTrigger>
					</TabsList>

					<!-- Active Rules Tab -->
					<TabsContent value="current" class="space-y-4">
						{#if isLoading}
							<div class="flex justify-center p-4">
								<div class="h-8 w-8 animate-spin rounded-full border-b-2 border-primary" />
							</div>
						{:else if activeAccessRules.length === 0}
							<Alert>
								<AlertTitle>No active rules</AlertTitle>
								<AlertDescription>
									Create new access rules to share your image securely.
								</AlertDescription>
							</Alert>
						{:else}
							<div class="custom-scrollbar max-h-[45vh] space-y-4 overflow-y-auto pr-2">
								{#each activeAccessRules as rule (rule.id)}
									<Card>
										<CardContent class="p-4">
											<div class="flex items-start justify-between gap-4">
												<div class="space-y-2">
													<div class="flex items-center gap-2">
														<h4 class="font-semibold">Access Rule</h4>
														<Badge variant="secondary">
															{rule.requires_password ? 'Password Protected' : 'Open Access'}
														</Badge>
													</div>

													<!-- Access Link -->
													<div class="flex items-center gap-2">
														<code class="rounded bg-muted px-2 py-1 text-sm">
															{rule.token}
														</code>
														<Button
															variant="ghost"
															size="sm"
															on:click={() => copyAccessLink(rule.token)}
														>
															<Link class="h-4 w-4" />
														</Button>
													</div>

													<!-- Allowed Emails -->
													{#if rule.allowed_emails.length > 0}
														<div class="flex flex-wrap gap-2">
															{#each rule.allowed_emails as email}
																<Badge variant="outline">{email}</Badge>
															{/each}
														</div>
													{/if}

													<!-- Stats & Features -->
													<div class="flex flex-wrap gap-3 text-sm text-muted-foreground">
														{#if rule.max_views > 0}
															<span class="flex items-center gap-1">
																<Eye class="h-4 w-4" />
																{rule.current_views}/{rule.max_views} views
															</span>
														{/if}
														{#if rule.allow_download}
															<span class="flex items-center gap-1">
																<Download class="h-4 w-4" />
																Downloads allowed
															</span>
														{/if}
														{#if rule.protection_features}
															{#each Object.entries(protectionStatus) as [key, status]}
																{#if rule.protection_features[key]}
																	<span class="flex items-center gap-1">
																		<svelte:component this={status.icon} class="h-4 w-4" />
																		{status.title}
																	</span>
																{/if}
															{/each}
														{/if}
													</div>
												</div>

												<Button
													variant="destructive"
													size="sm"
													on:click={() => deleteAccessRule(rule.id)}
												>
													<Trash2 class="h-4 w-4" />
												</Button>
											</div>
										</CardContent>
									</Card>
								{/each}
							</div>
						{/if}
					</TabsContent>

					<!-- Create New Rule Tab -->
					<TabsContent value="new" class="space-y-4">
						<div class="grid gap-4">
							<!-- Email Input -->
							<div class="space-y-2">
								<Label>Allowed Emails (Optional)</Label>
								<div class="flex gap-2">
									<Input
										type="email"
										placeholder="Add email address"
										bind:value={newAccess.emailInput}
										on:keydown={(e) => e.key === 'Enter' && addEmail()}
									/>
									<Button on:click={addEmail}>
										<Plus class="h-4 w-4" />
									</Button>
								</div>
								{#if newAccess.allowed_emails.length > 0}
									<div class="flex flex-wrap gap-2">
										{#each newAccess.allowed_emails as email}
											<Badge variant="secondary" class="flex items-center gap-1">
												{email}
												<button
													class="ml-1 text-muted-foreground hover:text-foreground"
													on:click={() => removeEmail(email)}
												>
													<X class="h-3 w-3" />
												</button>
											</Badge>
										{/each}
									</div>
								{/if}
							</div>

							<!-- Protection Features -->
							<div class="space-y-2">
								<Label>Protection Features</Label>
								<Card>
									<CardContent class="pt-4">
										<div class="grid gap-4">
											{#each Object.entries(protectionStatus) as [key, status]}
												<div class="flex items-start space-x-3">
													<div class="flex h-6 items-center">
														<Checkbox
															id={key}
															bind:checked={newAccess.protection_features[key]}
															disabled={!status.available}
														/>
													</div>
													<div class="space-y-1 leading-none">
														<div class="flex items-center">
															<Label
																for={key}
																class="flex items-center gap-2 {!status.available
																	? 'text-muted-foreground'
																	: ''}"
															>
																<svelte:component this={status.icon} class="h-4 w-4" />
																{status.title}
																{#if !status.available}
																	<Badge variant="outline" class="ml-2">Not Available</Badge>
																{/if}
															</Label>
														</div>
														<p class="text-sm text-muted-foreground">
															{status.description}
														</p>
													</div>
												</div>
											{/each}
										</div>
									</CardContent>
								</Card>
							</div>

							<!-- Password Protection -->
							<div class="space-y-2">
								<div class="flex items-center space-x-2">
									<Checkbox id="password-protection" bind:checked={newAccess.requires_password} />
									<Label for="password-protection">Password Protection</Label>
								</div>
								{#if newAccess.requires_password}
									<Input
										type="password"
										placeholder="Enter access password"
										bind:value={newAccess.password}
									/>
								{/if}
							</div>

							<!-- Additional Settings -->
							<div class="space-y-2">
								<div class="flex items-center space-x-2">
									<Checkbox id="allow-download" bind:checked={newAccess.allow_download} />
									<Label for="allow-download">Allow Download</Label>
								</div>
							</div>

							<div class="space-y-2">
								<Label>Max Views (0 for unlimited)</Label>
								<Input
									type="number"
									min="0"
									bind:value={newAccess.max_views}
									placeholder="Enter maximum views"
								/>
							</div>

							<Button class="w-full" on:click={createAccessRule} disabled={isSaving}>
								{#if isSaving}
									<div class="mr-2 h-4 w-4 animate-spin rounded-full border-b-2 border-white" />
								{/if}
								{isSaving ? 'Creating...' : 'Create Access Rule'}
							</Button>
						</div>
					</TabsContent>
				</Tabs>
			</CardContent>
		</Card>
	</div>
</div>

<style>
	/* Custom scrollbar styles */
	.custom-scrollbar {
		scrollbar-width: thin;
		scrollbar-color: hsl(var(--muted)) transparent;
	}

	.custom-scrollbar::-webkit-scrollbar {
		width: 6px;
	}

	.custom-scrollbar::-webkit-scrollbar-track {
		background: transparent;
	}

	.custom-scrollbar::-webkit-scrollbar-thumb {
		background-color: hsl(var(--muted));
		border-radius: 3px;
	}

	.custom-scrollbar::-webkit-scrollbar-thumb:hover {
		background-color: hsl(var(--muted-foreground));
	}
</style>
