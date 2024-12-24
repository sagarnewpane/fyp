<script>
	import * as Form from '$lib/components/ui/form';
	import { Input } from '$lib/components/ui/input';
	import { formSchema } from './schema';
	import { superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import * as Alert from '$lib/components/ui/alert';
	import FeatureCarousel from '$lib/components/FeatureCarousel.svelte';
	import { loginFeatures } from '$lib/config/features';

	export let data;

	const form = superForm(data, {
		validators: zodClient(formSchema)
	});
	const { form: formData, enhance, message } = form;
</script>

<div class="grid min-h-screen w-full lg:grid-cols-[40%_60%]">
	<div
		class="flex min-h-screen items-center justify-center bg-gradient-to-b from-primary/10 to-primary/5 px-4 py-8 lg:min-h-full"
	>
		<div class="relative w-full max-w-[450px] lg:max-w-[500px]">
			<div
				class="absolute -left-4 -top-4 h-full w-full rounded-lg border-2 border-primary/20"
			></div>
			<div class="relative mx-auto grid w-full gap-6 rounded-lg bg-white p-6 shadow-lg sm:p-8">
				<div class="grid gap-3 text-center">
					<h1 class="text-2xl font-bold sm:text-3xl">Login</h1>
					<p class="text-balance text-sm text-muted-foreground sm:text-base">
						Enter your email below to login to your account
					</p>
				</div>

				<form method="POST" use:enhance class="grid gap-5">
					{#if $message}
						<Alert.Root variant="destructive">
							<Alert.Title>Error</Alert.Title>
							<Alert.Description>{$message}</Alert.Description>
						</Alert.Root>
					{/if}

					<Form.Field {form} name="username">
						<Form.Control let:attrs>
							<div class="grid gap-2">
								<Form.Label>Username</Form.Label>
								<Input {...attrs} bind:value={$formData.username} />
							</div>
						</Form.Control>
						<Form.FieldErrors />
					</Form.Field>

					<Form.Field {form} name="password">
						<Form.Control let:attrs>
							<div class="grid gap-2">
								<div class="flex flex-wrap items-center justify-between gap-2">
									<Form.Label>Password</Form.Label>
									<a href="/forget-password" class="text-sm underline hover:text-primary">
										Forgot your password?
									</a>
								</div>
								<Input {...attrs} bind:value={$formData.password} type="password" />
							</div>
						</Form.Control>
						<Form.FieldErrors />
					</Form.Field>

					<Form.Button class="w-full">Login</Form.Button>

					<div class="text-center text-sm">
						Don't have an account?
						<a href="/register" class="ml-1 underline hover:text-primary">Sign up</a>
					</div>
				</form>
			</div>
		</div>
	</div>
	<FeatureCarousel features={loginFeatures} />
</div>
