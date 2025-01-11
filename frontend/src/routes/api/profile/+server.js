export async function GET({ fetch, cookies }) {
	const accessToken = cookies.get('access_token');

	if (!accessToken) {
		return new Response(JSON.stringify({ error: 'Not authenticated' }), {
			status: 401,
			headers: {
				'Content-Type': 'application/json'
			}
		});
	}

	try {
		const response = await fetch('http://localhost:8000/api/profile/', {
			headers: {
				Authorization: `Bearer ${accessToken}`
			}
		});

		if (response.ok) {
			const data = await response.json();
			return new Response(JSON.stringify(data), {
				headers: {
					'Content-Type': 'application/json'
				}
			});
		}

		return new Response(JSON.stringify({ error: 'Failed to fetch avatar' }), {
			status: response.status,
			headers: {
				'Content-Type': 'application/json'
			}
		});
	} catch (error) {
		return new Response(JSON.stringify({ error: 'Server error' }), {
			status: 500,
			headers: {
				'Content-Type': 'application/json'
			}
		});
	}
}

export async function POST({ request, fetch, cookies }) {
	const accessToken = cookies.get('access_token');

	if (!accessToken) {
		return new Response(JSON.stringify({ error: 'Not authenticated' }), {
			status: 401,
			headers: { 'Content-Type': 'application/json' }
		});
	}

	try {
		const formData = await request.formData();
		const file = formData.get('avatar');

		const apiFormData = new FormData();
		apiFormData.append('avatar', file);

		const response = await fetch('http://localhost:8000/api/profile/avatar/', {
			method: 'POST',
			headers: {
				Authorization: `Bearer ${accessToken}`
			},
			body: apiFormData
		});

		const data = await response.json();

		if (!response.ok) {
			throw new Error(data.error || 'Failed to upload avatar');
		}

		// Ensure we have the avatar_url before sending success response
		if (!data.avatar_url) {
			throw new Error('No avatar URL received from server');
		}

		return new Response(
			JSON.stringify({
				message: 'Avatar uploaded successfully',
				avatar_url: data.avatar_url
			}),
			{
				headers: { 'Content-Type': 'application/json' }
			}
		);
	} catch (error) {
		console.error('Avatar upload error:', error);
		return new Response(
			JSON.stringify({
				error: error.message || 'Server error'
			}),
			{
				status: error.status || 500,
				headers: { 'Content-Type': 'application/json' }
			}
		);
	}
}

export async function PATCH({ request, fetch, cookies }) {
	const accessToken = cookies.get('access_token');

	if (!accessToken) {
		return new Response(JSON.stringify({ error: 'Not authenticated' }), {
			status: 401,
			headers: { 'Content-Type': 'application/json' }
		});
	}

	try {
		const profileData = await request.json();

		const response = await fetch('http://localhost:8000/api/profile/', {
			method: 'PATCH',
			headers: {
				Authorization: `Bearer ${accessToken}`,
				'Content-Type': 'application/json'
			},
			body: JSON.stringify(profileData)
		});

		const data = await response.json();

		// Instead of throwing an error, return the response with the same status code
		return new Response(JSON.stringify(data), {
			status: response.status,
			headers: { 'Content-Type': 'application/json' }
		});
	} catch (error) {
		console.error('Profile update error:', error);
		return new Response(
			JSON.stringify({
				error: error.message || 'Server error'
			}),
			{
				status: 500,
				headers: { 'Content-Type': 'application/json' }
			}
		);
	}
}
