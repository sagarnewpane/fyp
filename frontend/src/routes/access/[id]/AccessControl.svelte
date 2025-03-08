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
		Brain,
		MoreVertical,
		Copy
	} from 'lucide-svelte';

	import {
		DropdownMenu,
		DropdownMenuTrigger,
		DropdownMenuContent,
		DropdownMenuItem,
		DropdownMenuSeparator
	} from '$lib/components/ui/dropdown-menu';

	// Props
	export let imageUrl;
	export let imageId;
	export let imageSecurity;

	// State
	let activeAccessRules = [];
	let isSaving = false;
	let isLoading = false;
	let newAccess = {
		access_name: '',
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
			access_name: '',
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
							<div class="flex justify-center p-6">
								<div
									class="h-10 w-10 animate-spin rounded-full border-4 border-primary border-t-transparent"
								/>
							</div>
						{:else if activeAccessRules.length === 0}
							<div class="flex flex-col items-center justify-center p-8 text-center">
								<Shield class="mb-4 h-12 w-12 text-muted-foreground" />
								<AlertTitle class="mb-2 text-xl font-semibold">No active rules</AlertTitle>
								<AlertDescription class="text-muted-foreground">
									Create new access rules to share your image securely.
								</AlertDescription>
							</div>
						{:else}
							<div class="custom-scrollbar max-h-[45vh] space-y-4 overflow-y-auto pr-2">
								{#each activeAccessRules as rule (rule.id)}
									<Card class="transition-all duration-200 hover:shadow-md">
										<CardContent class="p-5">
											<div class="flex flex-col gap-4">
												<!-- Header Section -->
												<div class="flex items-start justify-between">
													<div class="space-y-1">
														<h4 class="text-lg font-semibold tracking-tight">{rule.access_name}</h4>
														<Badge
															variant={rule.requires_password ? 'secondary' : 'outline'}
															class="font-medium"
														>
															{rule.requires_password ? '🔒 Password Protected' : '🔓 Open Access'}
														</Badge>
													</div>

													<DropdownMenu>
														<DropdownMenuTrigger>
															<Button variant="ghost" size="icon" class="h-8 w-8 p-0">
																<MoreVertical class="h-4 w-4" />
															</Button>
														</DropdownMenuTrigger>
														<DropdownMenuContent>
															<DropdownMenuItem on:click={() => copyAccessLink(rule.token)}>
																<Link class="mr-2 h-4 w-4" />
																<span>Copy link</span>
															</DropdownMenuItem>
															<DropdownMenuSeparator />
															<DropdownMenuItem
																class="text-destructive"
																on:click={() => deleteAccessRule(rule.id)}
															>
																<Trash2 class="mr-2 h-4 w-4" />
																<span>Delete</span>
															</DropdownMenuItem>
														</DropdownMenuContent>
													</DropdownMenu>
												</div>

												<!-- Access Link Section -->
												<div class="flex items-center gap-2 rounded-md bg-muted p-2">
													<code class="flex-1 overflow-x-auto whitespace-nowrap text-sm">
														{rule.token}
													</code>
													<Button
														variant="ghost"
														size="sm"
														class="shrink-0"
														on:click={() => copyAccessLink(rule.token)}
													>
														<Copy class="h-4 w-4" />
													</Button>
												</div>

												<!-- Allowed Emails Section -->
												{#if rule.allowed_emails && rule.allowed_emails.length > 0}
													<div class="space-y-2">
														<label class="text-xs font-medium text-muted-foreground">
															Authorized Emails
														</label>
														<div class="flex flex-wrap gap-2">
															{#each rule.allowed_emails as email}
																<Badge variant="secondary" class="flex items-center gap-1">
																	<Mail class="h-3 w-3" />
																	{email}
																</Badge>
															{/each}
														</div>
													</div>
												{/if}

												<!-- Stats & Features Section -->
												<div class="border-t pt-3">
													<div class="flex flex-wrap gap-4 text-sm text-muted-foreground">
														{#if rule.max_views > 0}
															<div class="flex items-center gap-2">
																<div class="rounded-full bg-muted p-1">
																	<Eye class="h-4 w-4" />
																</div>
																<span>{rule.current_views}/{rule.max_views} views</span>
															</div>
														{/if}
														{#if rule.allow_download}
															<div class="flex items-center gap-2">
																<div class="rounded-full bg-muted p-1">
																	<Download class="h-4 w-4" />
																</div>
																<span>Downloads allowed</span>
															</div>
														{/if}
														{#if rule.protection_features}
															{#each Object.entries(protectionStatus) as [key, status]}
																{#if rule.protection_features[key]}
																	<div class="flex items-center gap-2">
																		<div class="rounded-full bg-muted p-1">
																			<svelte:component this={status.icon} class="h-4 w-4" />
																		</div>
																		<span>{status.title}</span>
																	</div>
																{/if}
															{/each}
														{/if}
													</div>
												</div>
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
								<Label>Access Name (Optional)</Label>
								<div class="flex gap-2">
									<Input
										type="text"
										placeholder="Give a name to Access"
										bind:value={newAccess.access_name}
									/>
								</div>
							</div>
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
