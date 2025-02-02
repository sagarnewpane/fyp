export async function load({ params, fetch, cookies }) {
	const { id } = params;
	const accessToken = cookies.get('access_token');

	try {
		// Fetch the original image
		const imageRes = await fetch(`http://localhost:8000/image/${id}`, {
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

		// Fetch watermark settings
		const settingsRes = await fetch(`http://localhost:8000/api/image/${id}/watermark-settings/`, {
			headers: {
				Authorization: `Bearer ${accessToken}`
			}
		});

		const settings = settingsRes.ok ? await settingsRes.json() : null;

		return {
			status: 200,
			imageData,
			settings: settings
		};
	} catch (error) {
		console.error('Error loading watermark page:', error);
		return {
			status: 500,
			error: 'Server error'
		};
	}
}
