import { json } from '@sveltejs/kit';

// Delete access rule
export async function DELETE({ params, cookies }) {
	try {
		const { id, ruleId } = params;
		const accessToken = cookies.get('access_token');

		if (!accessToken) {
			return new Response('Unauthorized', { status: 401 });
		}

		const response = await fetch(`http://localhost:8000/images/${id}/access/${ruleId}/`, {
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

// Update access rule
export async function PATCH({ params, request, cookies }) {
	try {
		const { id, ruleId } = params;
		const accessToken = cookies.get('access_token');

		if (!accessToken) {
			return new Response('Unauthorized', { status: 401 });
		}

		const response = await fetch(`http://localhost:8000/images/${id}/access/${ruleId}/`, {
			method: 'PATCH',
			headers: {
				Authorization: `Bearer ${accessToken}`,
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(await request.json())
		});

		const data = await response.json();
		return json(data, { status: response.status });
	} catch (error) {
		console.error('Error updating access rule:', error);
		return json({ error: 'Failed to update access rule' }, { status: 500 });
	}
}
