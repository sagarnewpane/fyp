export async function fetchUserAvatar() {
	try {
		const response = await fetch('/api/avatar/', {
			credentials: 'include'
		});

		if (response.ok) {
			const data = await response.json();
			return data.avatar_url;
		}
		return null;
	} catch (error) {
		console.error('Failed to fetch avatar:', error);
		return null;
	}
}
