<script>
	import Form from './Form.svelte';
	export let data;
	import { API_ENDPOINTS } from '$lib/endpoints';
	console.log(API_ENDPOINTS.LOGIN);
</script>

<Form data={data.form} />
