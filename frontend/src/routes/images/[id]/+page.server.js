export async function load({ params, fetch, cookies }) {
	const { id } = params;
	const accessToken = cookies.get('access_token');

	try {
		const res = await fetch(`http://localhost:8000/image/${id}`, {
			method: 'GET',
			headers: {
				Authorization: `Bearer ${accessToken}`
			}
		});

		if (!res.ok) {
			// Return error data in a consistent format
			return {
				status: res.status,
				data: null,
				error: res.statusText || 'An unexpected error occurred'
			};
		}

		const data = await res.json();
		console.log(data);
		return {
			status: res.status,
			data,
			error: null
		};
	} catch (err) {
		// Handle network errors or other exceptions
		return {
			status: 500,
			data: null,
			error: 'An unexpected error occurred'
		};
	}
}
