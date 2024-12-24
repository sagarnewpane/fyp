import { superValidate, message } from 'sveltekit-superforms';
import { formSchema } from './schema';
import { zod } from 'sveltekit-superforms/adapters';
import { fail } from '@sveltejs/kit';
import { redirect } from 'sveltekit-flash-message/server';

export const load = async () => {
	return {
		form: await superValidate(zod(formSchema))
	};
};

export const actions = {
	default: async (event) => {
		const form = await superValidate(event, zod(formSchema));
		if (!form.valid) {
			return fail(400, { form });
		}

		const {
			username,
			password1: password,
			password2,
			email = '',
			first_name = '',
			last_name = ''
		} = form.data;

		let response;
		try {
			response = await fetch('http://localhost:8000/api/register/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					username,
					password,
					password2,
					email,
					first_name,
					last_name
				}),
				credentials: 'include'
			});
		} catch (error) {
			return message(
				form,
				'Unable to connect to the server. Please check your connection and try again.'
			);
		}

		if (!response.ok) {
			const errorData = await response.json();
			if (errorData && typeof errorData === 'object') {
				const [[field, [errorMessage]]] = Object.entries(errorData);
				return message(form, errorMessage || 'Registration failed. Please try again.');
			}
			return message(form, 'Registration failed. Please try again.');
		}

		const data = await response.json();
		console.log(data);

		throw redirect(
			'/login',
			{
				type: 'success',
				message: 'Registration successful!'
			},
			event
		);
	}
};
