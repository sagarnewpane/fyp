// src/lib/stores/auth.js
import { writable } from 'svelte/store';

export const authStore = writable({
	isAuthenticated: false,
	user: null,
	avatar: null
});
