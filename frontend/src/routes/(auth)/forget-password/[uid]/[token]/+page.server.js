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

		const { uid, token } = event.params;
		const { new_password, confirm_password } = form.data; // Add confirm_password here

		let response;
		try {
			response = await fetch('http://localhost:8000/api/password-reset-confirm/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					uidb64: uid,
					token,
					new_password,
					confirm_password
				})
			});
		} catch (error) {
			return message(form, 'Server is not reachable. Please try again later.');
		}

		if (!response.ok) {
			const data = await response.json();
			return message(form, data.error || 'Password reset failed');
		}

		return message(
			form,
			'Password has been reset successfully. You can now login with your new password.',
			{
				status: 'success'
			}
		);
	}
};
