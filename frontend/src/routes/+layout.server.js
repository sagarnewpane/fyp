import { loadFlashMessage } from 'sveltekit-flash-message/server';

export const load = loadFlashMessage(async ({ locals, depends }) => {
	depends('app:auth');
});
