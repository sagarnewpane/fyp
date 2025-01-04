import { error } from '@sveltejs/kit';

export async function load({ request, fetch, cookies, url }) {
	const accessToken = cookies.get('access_token');
	const page = parseInt(url.searchParams.get('page')) || 1;
	const search = url.searchParams.get('search') || '';

	if (!accessToken) {
		throw error(401, 'Unauthorized');
	}

	try {
		const params = new URLSearchParams();
		params.set('page', page.toString());
		if (search) {
			params.set('search', search);
		}

		const res = await fetch(`http://localhost:8000/images/?${params.toString()}`, {
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

		// Return the data directly without additional wrapping
		return {
			images: data
		};
	} catch (err) {
		console.error('Error fetching images:', err);
		throw error(500, 'Failed to fetch images');
	}
}
