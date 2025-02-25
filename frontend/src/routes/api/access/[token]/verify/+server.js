import { json } from '@sveltejs/kit';

export async function POST({ params, request }) {
	try {
		const { token } = params;
		const data = await request.json();

		const response = await fetch(`http://localhost:8000/access/${token}/verify/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		});

		const responseData = await response.json();

		if (!response.ok) {
			return json(
				{ error: responseData.error || 'Failed to verify access' },
				{ status: response.status }
			);
		}

		return json(responseData);
	} catch (error) {
		console.error('Error verifying access:', error);
		return json({ error: 'Internal server error' }, { status: 500 });
	}
}
