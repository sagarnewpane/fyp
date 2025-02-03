import { json } from '@sveltejs/kit';

// GET - Retrieve invisible watermark
export async function GET({ params, cookies }) {
	try {
		const { id } = params;
		const accessToken = cookies.get('access_token');

		if (!accessToken) {
			return new Response('Unauthorized', { status: 401 });
		}

		const response = await fetch(`http://localhost:8000/api/image/${id}/invisible-watermark/`, {
			method: 'GET',
			headers: {
				Authorization: `Bearer ${accessToken}`,
				'Content-Type': 'application/json'
			}
		});

		const data = await response.json();
		return json(data, { status: response.status });
	} catch (error) {
		console.error('Error fetching invisible watermark:', error);
		return json({ error: 'Failed to fetch invisible watermark' }, { status: 500 });
	}
}

// POST - Create new invisible watermark
export async function POST({ params, request, cookies }) {
	try {
		const { id } = params;
		const accessToken = cookies.get('access_token');

		if (!accessToken) {
			return new Response('Unauthorized', { status: 401 });
		}

		const response = await fetch(`http://localhost:8000/api/image/${id}/invisible-watermark/`, {
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
		console.error('Error creating invisible watermark:', error);
		return json({ error: 'Failed to create invisible watermark' }, { status: 500 });
	}
}

// PATCH - Update existing invisible watermark
export async function PATCH({ params, request, cookies }) {
	try {
		const { id } = params;
		const accessToken = cookies.get('access_token');

		if (!accessToken) {
			return new Response('Unauthorized', { status: 401 });
		}

		const response = await fetch(`http://localhost:8000/api/image/${id}/invisible-watermark/`, {
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
		console.error('Error updating invisible watermark:', error);
		return json({ error: 'Failed to update invisible watermark' }, { status: 500 });
	}
}

// DELETE - Remove invisible watermark
export async function DELETE({ params, cookies }) {
	try {
		const { id } = params;
		const accessToken = cookies.get('access_token');

		if (!accessToken) {
			return new Response('Unauthorized', { status: 401 });
		}

		const response = await fetch(`http://localhost:8000/api/image/${id}/invisible-watermark/`, {
			method: 'DELETE',
			headers: {
				Authorization: `Bearer ${accessToken}`
			}
		});

		// For DELETE, we might not have any content to return
		if (response.status === 204) {
			return new Response(null, { status: 204 });
		}

		const data = await response.json();
		return json(data, { status: response.status });
	} catch (error) {
		console.error('Error deleting invisible watermark:', error);
		return json({ error: 'Failed to delete invisible watermark' }, { status: 500 });
	}
}
