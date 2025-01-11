import { authStore } from '$lib/stores/auth';

export async function fetchUserAvatar() {
	try {
		const response = await fetch('/api/profile/', {
			credentials: 'include'
		});

		if (response.ok) {
			const data = await response.json();
			const avatarUrl = data.avatar_url;

			// Update the auth store
			authStore.update((state) => ({
				...state,
				avatar: avatarUrl
			}));

			return avatarUrl;
		}
		return null;
	} catch (error) {
		console.error('Failed to fetch avatar:', error);
		return null;
	}
}
