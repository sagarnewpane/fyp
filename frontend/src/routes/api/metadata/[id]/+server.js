import { json } from '@sveltejs/kit';

// Get metadata for an image
export async function GET({ params, cookies }) {
	try {
		const { id } = params;
		const accessToken = cookies.get('access_token');

		if (!accessToken) {
			return new Response('Unauthorized', { status: 401 });
		}

		const response = await fetch(`http://localhost:8000/image/${id}/metadata/`, {
			headers: {
				Authorization: `Bearer ${accessToken}`
			}
		});

		const data = await response.json();
		return json(data, { status: response.status });
	} catch (error) {
		console.error('Error fetching metadata:', error);
		return json({ error: 'Failed to fetch metadata' }, { status: 500 });
	}
}

// Update metadata (single field)
export async function PATCH({ params, request, cookies }) {
	try {
		const { id } = params;
		const accessToken = cookies.get('access_token');

		if (!accessToken) {
			return new Response('Unauthorized', { status: 401 });
		}

		const response = await fetch(`http://localhost:8000/image/${id}/metadata/`, {
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
		console.error('Error updating metadata:', error);
		return json({ error: 'Failed to update metadata' }, { status: 500 });
	}
}

// Bulk update metadata
export async function PUT({ params, request, cookies }) {
	try {
		const { id } = params;
		const accessToken = cookies.get('access_token');

		if (!accessToken) {
			return new Response('Unauthorized', { status: 401 });
		}

		const response = await fetch(`http://localhost:8000/image/${id}/metadata/`, {
			method: 'PUT',
			headers: {
				Authorization: `Bearer ${accessToken}`,
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(await request.json())
		});

		const data = await response.json();
		return json(data, { status: response.status });
	} catch (error) {
		console.error('Error bulk updating metadata:', error);
		return json({ error: 'Failed to bulk update metadata' }, { status: 500 });
	}
}

// Delete metadata field
export async function DELETE({ params, url, cookies }) {
	try {
		const { id } = params;
		const accessToken = cookies.get('access_token');

		if (!accessToken) {
			return new Response('Unauthorized', { status: 401 });
		}

		// Get query parameters
		const type = url.searchParams.get('type') || 'custom';
		const field = url.searchParams.get('field');

		if (!field) {
			return json({ error: 'Field parameter is required' }, { status: 400 });
		}

		const response = await fetch(
			`http://localhost:8000/image/${id}/metadata/?type=${type}&field=${field}`,
			{
				method: 'DELETE',
				headers: {
					Authorization: `Bearer ${accessToken}`
				}
			}
		);

		if (response.status === 204) {
			return new Response(null, { status: 204 });
		}

		const data = await response.json();
		return json(data, { status: response.status });
	} catch (error) {
		console.error('Error deleting metadata field:', error);
		return json({ error: 'Failed to delete metadata field' }, { status: 500 });
	}
}

// Add custom metadata field
export async function POST({ params, request, cookies }) {
	try {
		const { id } = params;
		const accessToken = cookies.get('access_token');

		if (!accessToken) {
			return new Response('Unauthorized', { status: 401 });
		}

		const response = await fetch(`http://localhost:8000/image/${id}/metadata/custom/`, {
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
		console.error('Error adding custom metadata:', error);
		return json({ error: 'Failed to add custom metadata' }, { status: 500 });
	}
}
