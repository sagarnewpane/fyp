<script>
	import '../app.css';
	import Footer from '$lib/components/Footer.svelte';
	import Navbar from '$lib/components/Navbar.svelte';
	import { Toaster } from '$lib/components/ui/sonner';
	import { initFlash } from 'sveltekit-flash-message/client';
	import { page } from '$app/stores';
	import { toast } from 'svelte-sonner';
	import { authStore } from '$lib/stores/auth';

	export let data = {
		isAuthenticated: false,
		user: null
	};

	// Update store whenever data changes
	$: {
		const authData = {
			isAuthenticated: Boolean(data?.isAuthenticated),
			user: data?.user || null
		};

		// console.log('Updating auth store with:', authData);
		authStore.set(authData);
	}

	const flash = initFlash(page);

	// Handle flash messages
	$: if ($flash) {
		const { type, message } = $flash;
		console.log(message);
		switch (type) {
			case 'success':
				toast.success(message);
				break;
			case 'error':
				toast.error(message);
				break;
			case 'info':
				toast.info(message);
				break;
		}
	}
</script>

<Navbar />
<Toaster />
<slot />
<Footer />
