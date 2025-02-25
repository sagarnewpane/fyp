import { json } from '@sveltejs/kit';

// Initialize access
export async function POST({ params, request }) {
	try {
		const { token } = params;
		const data = await request.json();

		const response = await fetch(`http://localhost:8000/access/${token}/initiate/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		});

		const responseData = await response.json();

		if (!response.ok) {
			return json(
				{ error: responseData.error || 'Failed to initiate access' },
				{ status: response.status }
			);
		}

		return json(responseData);
	} catch (error) {
		console.error('Error initiating access:', error);
		return json({ error: 'Internal server error' }, { status: 500 });
	}
}
