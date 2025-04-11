import { json } from '@sveltejs/kit';
export async function POST({ params, request }) {
	try {
		const { token } = params;
		const data = await request.json();

		const response = await fetch(`http://localhost:8000/access/${token}/request/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		});

		const responseData = await response.json();

		if (!response.ok) {
			return json(
				{ error: responseData.error || 'Failed to submit access request' },
				{ status: response.status }
			);
		}

		return json(responseData);
	} catch (error) {
		console.error('Error requesting access:', error);
		return json(
			{ error: error.message || 'Internal server error during access request' },
			{ status: 500 }
		);
	}
}
