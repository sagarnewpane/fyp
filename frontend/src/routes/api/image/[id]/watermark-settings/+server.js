import { json } from '@sveltejs/kit';

export async function PATCH({ params, request, cookies }) {
	try {
		const { id } = params;
		const accessToken = cookies.get('access_token');

		if (!accessToken) {
			return new Response('Unauthorized', { status: 401 });
		}

		// Forward the request to Django backend
		const response = await fetch(`http://localhost:8000/api/image/${id}/watermark-settings/`, {
			method: 'PATCH',
			headers: {
				Authorization: `Bearer ${accessToken}`,
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(await request.json())
		});

		// Get the response data
		const data = await response.json();

		// Return the response with the same status code
		return json(data, { status: response.status });
	} catch (error) {
		console.error('Error updating watermark settings:', error);
		return json({ error: 'Failed to update watermark settings' }, { status: 500 });
	}
}
