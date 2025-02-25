import { json } from '@sveltejs/kit';

// Get access rules for an image
export async function GET({ params, cookies }) {
	try {
		const { id } = params;
		const accessToken = cookies.get('access_token');

		if (!accessToken) {
			return new Response('Unauthorized', { status: 401 });
		}

		const response = await fetch(`http://localhost:8000/images/${id}/access/`, {
			headers: {
				Authorization: `Bearer ${accessToken}`
			}
		});

		const data = await response.json();
		return json(data, { status: response.status });
	} catch (error) {
		console.error('Error fetching access rules:', error);
		return json({ error: 'Failed to fetch access rules' }, { status: 500 });
	}
}

// Create new access rule
export async function POST({ params, request, cookies }) {
	try {
		const { id } = params;
		const accessToken = cookies.get('access_token');

		if (!accessToken) {
			return new Response('Unauthorized', { status: 401 });
		}

		const response = await fetch(`http://localhost:8000/images/${id}/access/`, {
			method: 'POST',
			headers: {
				Authorization: `Bearer ${accessToken}`,
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(await request.json())
		});

		const data = await response.json();
		return json(data, { status: response.status });
	} catch (error) {
		console.error('Error creating access rule:', error);
		return json({ error: 'Failed to create access rule' }, { status: 500 });
	}
}
