import { json } from '@sveltejs/kit';

// GET - Fetch access requests
export async function GET({ request, cookies }) {
	try {
		const accessToken = cookies.get('access_token');

		if (!accessToken) {
			return json({ error: 'Unauthorized' }, { status: 401 });
		}

		const response = await fetch('http://localhost:8000/access-requests/', {
			method: 'GET',
			headers: {
				Authorization: `Bearer ${accessToken}`,
				'Content-Type': 'application/json'
			}
		});

		if (!response.ok) {
			const error = await response.json();
			return json(error, { status: response.status });
		}

		const data = await response.json();
		return json(data);
	} catch (error) {
		console.error('Error fetching access requests:', error);
		return json({ error: 'Failed to fetch access requests' }, { status: 500 });
	}
}

// POST - Handle approve/deny actions
export async function POST({ request, cookies, params }) {
	try {
		const accessToken = cookies.get('access_token');

		if (!accessToken) {
			return json({ error: 'Unauthorized' }, { status: 401 });
		}

		const { requestId, action } = await request.json();

		const response = await fetch(`http://localhost:8000/access-requests/${requestId}/`, {
			method: 'POST',
			headers: {
				Authorization: `Bearer ${accessToken}`,
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({ action })
		});

		if (!response.ok) {
			const error = await response.json();
			return json(error, { status: response.status });
		}

		const data = await response.json();
		return json(data);
	} catch (error) {
		console.error('Error handling access request action:', error);
		return json({ error: 'Failed to process request' }, { status: 500 });
	}
}
