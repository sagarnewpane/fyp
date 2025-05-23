import { error } from '@sveltejs/kit';
import { API_ENDPOINTS } from '$lib/endpoints';

export async function load({ request, fetch, cookies, url, depends }) {
	const accessToken = cookies.get('access_token');
	if (!accessToken) {
		throw error(401, 'Unauthorized');
	}

	try {
		// Get all query parameters
		const params = new URLSearchParams(url.searchParams);

		depends('data:images');

		const res = await fetch(`${API_ENDPOINTS.IMAGES}?${params.toString()}`, {
			method: 'GET',
			headers: {
				Authorization: `Bearer ${accessToken}`,
				'Content-Type': 'application/json'
			}
		});

		if (!res.ok) {
			throw error(res.status, 'Failed to fetch images');
		}

		const data = await res.json();
		return { images: data };
	} catch (err) {
		console.error('Error fetching images:', err);
		throw error(500, 'Failed to fetch images');
	}
}
