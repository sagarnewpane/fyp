import { redirect } from 'sveltekit-flash-message/server';

export async function POST(event) {
	event.cookies.delete('access_token', { path: '/' });
	event.cookies.delete('refresh_token', { path: '/' });

	throw redirect(
		'',
		{
			type: 'success',
			message: 'Logout Successful!'
		},
		event
	);
}
