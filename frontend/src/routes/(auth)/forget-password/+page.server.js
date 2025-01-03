import { superValidate, message } from 'sveltekit-superforms';
import { formSchema } from './schema';
import { zod } from 'sveltekit-superforms/adapters';
import { fail } from '@sveltejs/kit';

export const load = async () => {
	return {
		form: await superValidate(zod(formSchema))
	};
};

export const actions = {
	default: async (event) => {
		const form = await superValidate(event, zod(formSchema));
		if (!form.valid) {
			return fail(400, {
				form
			});
		}

		const email = form.data.email;

		try {
			const response = await fetch('http://localhost:8000/api/password-reset/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					email
				})
			});

			const data = await response.json();

			if (!response.ok) {
				// Check for email-specific error
				if (data.email) {
					return message(form, {
						status: 'error',
						text: data.email[0]
					});
				}
				// Fall back to other error messages
				return message(form, {
					status: 'error',
					text: data.error || data.detail || 'Password reset request failed'
				});
			}

			return message(form, {
				status: 'success',
				text: 'Password reset link has been sent to your email.'
			});
		} catch (error) {
			return message(form, {
				status: 'error',
				text: 'Server is not reachable. Please try again later.'
			});
		}
	}
};
