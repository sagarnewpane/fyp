import { json } from '@sveltejs/kit';

// Fetch an Image
export async function GET({ params, cookies }) {
	try {
		const { id } = params;
		const accessToken = cookies.get('access_token');

		if (!accessToken) {
			return new Response('Unauthorized', { status: 401 });
		}

		const response = await fetch(`http://localhost:8000/image/${id}/`, {
			method: 'GET',
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
		console.error('Error fetching image:', error);
		return json({ error: 'Error fetching image' }, { status: 500 });
	}
}

// Delete an image
export async function DELETE({ params, cookies }) {
	try {
		const { id, ruleId } = params;
		const accessToken = cookies.get('access_token');

		if (!accessToken) {
			return new Response('Unauthorized', { status: 401 });
		}

		const response = await fetch(`http://localhost:8000/image/${id}/`, {
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
		console.error('Error deleting access rule:', error);
		return json({ error: 'Failed to delete access rule' }, { status: 500 });
	}
}
