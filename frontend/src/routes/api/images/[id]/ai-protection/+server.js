import { json } from '@sveltejs/kit';

// Get AI protection status
export async function GET({ params, cookies }) {
	try {
		const { id } = params;
		const accessToken = cookies.get('access_token');

		if (!accessToken) {
			return new Response('Unauthorized', { status: 401 });
		}

		const response = await fetch(`http://localhost:8000/images/${id}/ai-protection/`, {
			method: 'GET',
			headers: {
				Authorization: `Bearer ${accessToken}`
			}
		});

		const data = await response.json();
		return json(data, { status: response.status });
	} catch (error) {
		console.error('Error fetching AI protection status:', error);
		return json({ error: 'Error fetching AI protection status' }, { status: 500 });
	}
}

// Apply AI protection
export async function POST({ params, cookies }) {
	try {
		const { id } = params;
		const accessToken = cookies.get('access_token');

		if (!accessToken) {
			return new Response('Unauthorized', { status: 401 });
		}

		const response = await fetch(`http://localhost:8000/images/${id}/ai-protection/`, {
			method: 'POST',
			headers: {
				Authorization: `Bearer ${accessToken}`,
				'Content-Type': 'application/json'
			}
		});

		const data = await response.json();
		return json(data, { status: response.status });
	} catch (error) {
		console.error('Error applying AI protection:', error);
		return json({ error: 'Error applying AI protection' }, { status: 500 });
	}
}

// Remove AI protection
export async function DELETE({ params, cookies }) {
	try {
		const { id } = params;
		const accessToken = cookies.get('access_token');

		if (!accessToken) {
			return new Response('Unauthorized', { status: 401 });
		}

		const response = await fetch(`http://localhost:8000/images/${id}/ai-protection/`, {
			method: 'DELETE',
			headers: {
				Authorization: `Bearer ${accessToken}`
			}
		});

		if (response.status === 204) {
			return new Response(null, { status: 204 });
		}

		const data = await response.json();
		return json(data, { status: response.status });
	} catch (error) {
		console.error('Error removing AI protection:', error);
		return json({ error: 'Error removing AI protection' }, { status: 500 });
	}
} 