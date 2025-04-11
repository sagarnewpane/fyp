import { json } from '@sveltejs/kit';

// Initialize access
export async function POST({ params, request }) {
	try {
		const { token } = params;
		const data = await request.json();
		console.log('Server route received:', { token, data }); // Add this

		const response = await fetch(`http://localhost:8000/access/${token}/initiate/`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(data)
		});

		console.log('Django response status:', response.status); // Add this
		const responseData = await response.json();
		console.log('Django response data:', responseData); // Add this

		if (!response.ok) {
			return json(
				{ error: responseData.error || 'Failed to initiate access' },
				{ status: response.status }
			);
		}

		return json(responseData);
	} catch (error) {
		console.error('Error initiating access:', error);
		return json(
			{ error: error.message || 'Internal server error during access initiation' },
			{ status: 500 }
		);
	}
}
