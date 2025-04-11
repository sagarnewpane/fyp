import { json } from '@sveltejs/kit';

export async function POST({ params, request, cookies }) {
	try {
		const accessToken = cookies.get('access_token');
		const { requestId } = params;

		if (!accessToken) {
			return json({ error: 'Unauthorized' }, { status: 401 });
		}

		const body = await request.json();

		const response = await fetch(`http://localhost:8000/access-requests/${requestId}/`, {
			method: 'POST',
			headers: {
				Authorization: `Bearer ${accessToken}`,
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(body)
		});

		if (!response.ok) {
			const error = await response.json();
			return json(error, { status: response.status });
		}

		const data = await response.json();
		return json(data);
	} catch (error) {
		console.error('Error processing access request:', error);
		return json({ error: 'Failed to process request' }, { status: 500 });
	}
}
