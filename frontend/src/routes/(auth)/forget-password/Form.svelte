<script>
	import * as Form from '$lib/components/ui/form';
	import { Input } from '$lib/components/ui/input';
	import { formSchema } from './schema';
	import { superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import * as Alert from '$lib/components/ui/alert';
	import { Button } from '$lib/components/ui/button/index.js';

	export let data;

	const form = superForm(data, {
		validators: zodClient(formSchema)
	});
	const { form: formData, enhance, message } = form;
</script>

<div class="grid min-h-screen w-full lg:grid-cols-2">
	<div
		class="flex min-h-screen items-center justify-center bg-gradient-to-b from-primary/10 to-primary/5 px-4 py-8 lg:min-h-full"
	>
		<div class="relative w-full max-w-[450px] lg:max-w-[500px]">
			<div
				class="absolute -left-4 -top-4 h-full w-full rounded-lg border-2 border-primary/20"
			></div>
			<div class="relative mx-auto grid w-full gap-6 rounded-lg bg-white p-6 shadow-lg sm:p-8">
				<div class="grid gap-3 text-center">
					<h1 class="text-2xl font-bold sm:text-3xl">Forgot Password</h1>
					<p class="text-balance text-sm text-muted-foreground sm:text-base">
						Enter your email and we'll send you a link to reset your password
					</p>
				</div>

				<form method="POST" use:enhance class="grid gap-5">
					{#if $message}
						<Alert.Root variant={$message.status === 'success' ? 'default' : 'destructive'}>
							<Alert.Title>{$message.status === 'success' ? 'Success' : 'Error'}</Alert.Title>
							<Alert.Description>{$message}</Alert.Description>
						</Alert.Root>
					{/if}

					<Form.Field {form} name="email">
						<Form.Control let:attrs>
							<div class="grid gap-2">
								<Form.Label>Email</Form.Label>
								<Input {...attrs} bind:value={$formData.email} type="email" />
							</div>
						</Form.Control>
						<Form.FieldErrors />
					</Form.Field>

					<Form.Button className="w-full">Send Reset Link</Form.Button>

					<div class="mt-2 text-center text-sm">
						Remember your password?
						<a href="/login" class="ml-1 underline hover:text-primary">Login</a>
					</div>
				</form>
			</div>
		</div>
	</div>
	<div class="hidden h-screen lg:block">
		<img
			src="/side.webp"
			alt="placeholder"
			class="h-full w-full object-cover dark:brightness-[0.2] dark:grayscale"
		/>
	</div>
</div>
