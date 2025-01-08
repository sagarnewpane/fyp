import { error } from '@sveltejs/kit';

export async function load({ request, fetch, cookies, url }) {
	const accessToken = cookies.get('access_token');
	if (!accessToken) {
		throw error(401, 'Unauthorized');
	}

	try {
		const res = await fetch(`http://localhost:8000/images/?sort=-created_at&page=1`, {
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
		const recent = data.results.slice(0, 4);
		return { images: recent };
	} catch (err) {
		console.error('Error fetching images:', err);
		throw error(500, 'Failed to fetch images');
	}
}
