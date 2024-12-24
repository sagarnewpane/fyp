<script>
	import '../app.css';
	import Footer from '$lib/components/Footer.svelte';
	import Navbar from '$lib/components/Navbar.svelte';
	import { initFlash } from 'sveltekit-flash-message/client';
	import { page } from '$app/stores';
	import { toast } from 'svelte-sonner';

	const flash = initFlash(page);

	// Handle flash messages
	$: if ($flash) {
		const { type, message } = $flash;
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
<slot />
<Footer />
