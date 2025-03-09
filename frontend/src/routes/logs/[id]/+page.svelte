<script>
	import ImageLog from './ImageLog.svelte';
	import { page } from '$app/stores';

	const imageId = $page.params.id;
</script>

<ImageLog {imageId} />
