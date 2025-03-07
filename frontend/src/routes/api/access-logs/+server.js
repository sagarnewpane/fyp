import { json } from '@sveltejs/kit';

// GET - Retrieve invisible watermark
export async function GET({ params, cookies }) {
	try {
		const { id } = params;
		const accessToken = cookies.get('access_token');

		if (!accessToken) {
			return new Response('Unauthorized', { status: 401 });
		}

		const response = await fetch(`http://localhost:8000/access-logs/`, {
			method: 'GET',
			headers: {
				Authorization: `Bearer ${accessToken}`,
				'Content-Type': 'application/json'
			}
		});

		const data = await response.json();
		return json(data, { status: response.status });
	} catch (error) {
		console.error('Error fetching invisible watermark:', error);
		return json({ error: 'Failed to fetch invisible watermark' }, { status: 500 });
	}
}
