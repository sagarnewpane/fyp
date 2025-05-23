import { error, json } from '@sveltejs/kit';
import { API_ENDPOINTS } from '$lib/endpoints';

export async function POST({ request, cookies }) {
	try {
		const formData = await request.formData();
		const image = formData.get('image');
		const accessToken = cookies.get('access_token');

		if (!accessToken) {
			throw error(401, 'Unauthorized');
		}

		const res = await fetch(API_ENDPOINTS.UPLOAD, {
			method: 'POST',
			headers: {
				Authorization: `Bearer ${accessToken}`
			},
			body: formData
		});

		if (res.ok) {
			const result = await res.json();
			return json(result);
		} else {
			throw error(res.status, 'Failed to upload image');
		}
	} catch (err) {
		console.error('Error uploading image:', err);
		throw error(500, 'Internal Server Error');
	}
}
