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
