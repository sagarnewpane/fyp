import { loadFlashMessage } from 'sveltekit-flash-message/server';

export const load = loadFlashMessage(async ({ locals, depends }) => {
	depends('app:auth');

	// Ensure we have default values
	const data = {
		isAuthenticated: locals.isAuthenticated || false,
		user: locals.user || null
	};

	return data;
});
