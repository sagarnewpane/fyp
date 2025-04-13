// hooks.server.js
import { redirect } from '@sveltejs/kit';

const CONFIG = {
	PROTECTED_ROUTES: ['/images', '/profile', '/user', '/watermark', '/logs', '/access', '/metadata'],
	API_ENDPOINTS: {
		VERIFY: 'http://localhost:8000/verify/',
		REFRESH: 'http://localhost:8000/token/refresh/'
		// AVATAR: 'http://localhost:8000/avatar'
	},
	COOKIE_OPTIONS: {
		access: {
			httpOnly: true,
			path: '/',
			maxAge: 300,
			secure: true,
			sameSite: 'lax'
		},
		refresh: {
			httpOnly: true,
			path: '/',
			maxAge: 604800,
			secure: true,
			sameSite: 'lax'
		}
	}
};

/** @type {import('@sveltejs/kit').Handle} */
export async function handle({ event, resolve }) {
	const authResult = await authenticateRequest(event);

	// Set authentication data in locals for server-side access
	event.locals.user = authResult.user;
	event.locals.isAuthenticated = authResult.isAuthenticated;
	// event.locals.avatar = authResult.avatar || null;

	const isProtectedRoute = CONFIG.PROTECTED_ROUTES.some((route) =>
		event.url.pathname.startsWith(route)
	);

	if (isProtectedRoute && !authResult.isAuthenticated) {
		const redirectUrl = `/login`;
		throw redirect(303, redirectUrl);
	}

	const response = await resolve(event);
	return response;
}

async function authenticateRequest(event) {
	try {
		const accessToken = event.cookies.get('access_token');
		const refreshToken = event.cookies.get('refresh_token');

		// Try access token first
		if (accessToken) {
			const userData = await verifyToken(accessToken);
			if (userData) {
				return {
					isAuthenticated: true,
					user: userData
					// avatar: await fetchUserAvatar(accessToken, event)
				};
			}
		}

		// Try refresh token if access token failed
		if (refreshToken) {
			const newTokens = await refreshAccessToken(refreshToken);
			if (newTokens) {
				setCookies(event, newTokens);
				const userData = await verifyToken(newTokens.access);

				if (userData) {
					return {
						isAuthenticated: true,
						user: userData
						// avatar: await fetchUserAvatar(newTokens.access, event)
					};
				}
			}
		}

		// Clear cookies if authentication failed
		clearCookies(event);
		return {
			isAuthenticated: false,
			user: null,
			avatar: null
		};
	} catch (error) {
		console.error('Authentication error:', error);
		clearCookies(event);
		return {
			isAuthenticated: false,
			user: null,
			avatar: null
		};
	}
}

// Remaining functions (verifyToken, refreshAccessToken, setCookies, clearCookies) remain unchanged
async function verifyToken(token) {
	try {
		const response = await fetch(CONFIG.API_ENDPOINTS.VERIFY, {
			headers: { Authorization: `Bearer ${token}` }
		});
		return response.ok ? await response.json() : null;
	} catch {
		return null;
	}
}

async function refreshAccessToken(refreshToken) {
	try {
		const response = await fetch(CONFIG.API_ENDPOINTS.REFRESH, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ refresh: refreshToken })
		});
		return response.ok ? await response.json() : null;
	} catch {
		return null;
	}
}

function setCookies(event, tokens) {
	event.cookies.set('access_token', tokens.access, CONFIG.COOKIE_OPTIONS.access);
	if (tokens.refresh) {
		event.cookies.set('refresh_token', tokens.refresh, CONFIG.COOKIE_OPTIONS.refresh);
	}
}

function clearCookies(event) {
	event.cookies.delete('access_token', { path: '/' });
	event.cookies.delete('refresh_token', { path: '/' });
}
