export async function POST({ request, fetch, cookies }) {
	const accessToken = cookies.get('access_token');

	if (!accessToken) {
		return new Response(JSON.stringify({ error: 'Not authenticated' }), {
			status: 401,
			headers: { 'Content-Type': 'application/json' }
		});
	}

	const response = await fetch('http://127.0.0.1:8000/api/password/change/', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${accessToken}`
		},
		body: await request.text()
	});

	console.log(response);

	return new Response(await response.text(), {
		status: response.status,
		headers: response.headers
	});
}
