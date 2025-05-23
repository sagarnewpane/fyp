import { API_ENDPOINTS } from '$lib/endpoints';

export async function load({ params, fetch, cookies }) {
	const { id } = params;
	const accessToken = cookies.get('access_token');

	try {
		// Fetch the original image
		const imageRes = await fetch(API_ENDPOINTS.IMAGE(id), {
			headers: {
				Authorization: `Bearer ${accessToken}`
			}
		});

		if (!imageRes.ok) {
			return {
				status: imageRes.status,
				error: 'Failed to load image'
			};
		}

		const imageData = await imageRes.json();

		return {
			status: 200,
			imageData
		};
	} catch (error) {
		console.error('Error loading watermark page:', error);
		return {
			status: 500,
			error: 'Server error'
		};
	}
}
