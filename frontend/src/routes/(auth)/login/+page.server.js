import { superValidate, message } from 'sveltekit-superforms';
import { formSchema } from './schema';
import { zod } from 'sveltekit-superforms/adapters';
import { fail } from '@sveltejs/kit';
// import { redirect } from 'sveltekit-flash-message/server';

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

		const username = form.data.username;
		const password = form.data.password;

		let response;
		try {
			response = await fetch('http://localhost:8000/api/token/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					username,
					password
				})
			});
		} catch (error) {
			return message(form, 'Server is not reachable. Please try again later.');
		}

		const data = await response.json();

		if (!response.ok) {
			return message(form, data.detail || 'Login failed');
		}

		// If login is successful, set cookies and redirect
		event.cookies.set('access_token', data.access, {
			httpOnly: true,
			path: '/',
			maxAge: 60 * 5 // 5 minutes for access token
		});

		event.cookies.set('refresh_token', data.refresh, {
			httpOnly: true,
			path: '/',
			maxAge: 60 * 60 * 24 * 7 // 7 days for refresh token
		});

		// throw redirect(
		// 	'/',
		// 	{
		// 		type: 'success',
		// 		message: 'Login Successful!'
		// 	},
		// 	event
		// );
	}
};
