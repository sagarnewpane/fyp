<script>
	import { cn } from "$lib/utils.js";
	import { Eye, EyeOff } from 'lucide-svelte';
	let className = undefined;
	export let value = undefined;
	export { className as class };
	export let readonly = undefined;

	// Password visibility toggle
	export let type = 'text';
	let showPassword = false;

	$: inputType = type === 'password' && showPassword ? 'text' : type;
</script>

<div class="relative">
	<input
		class={cn(
			"border-input placeholder:text-muted-foreground focus-visible:ring-ring flex h-9 w-full rounded-md border bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 file:bg-transparent file:text-sm file:font-medium focus-visible:outline-none focus-visible:ring-1 disabled:cursor-not-allowed disabled:opacity-50 pr-10", // add pr-10 for icon space
			className
		)}
		bind:value
		{readonly}
		type={inputType}
		on:blur
		on:change
		on:click
		on:focus
		on:focusin
		on:focusout
		on:keydown
		on:keypress
		on:keyup
		on:mouseover
		on:mouseenter
		on:mouseleave
		on:mousemove
		on:paste
		on:input
		on:wheel|passive
		{...$$restProps}
	/>
	{#if type === 'password'}
		<button type="button" tabindex="-1" class="absolute right-2 top-1/2 -translate-y-1/2 p-1 text-muted-foreground hover:text-foreground focus:outline-none" on:click={() => showPassword = !showPassword}>
			{#if showPassword}
				<EyeOff class="h-5 w-5" />
			{:else}
				<Eye class="h-5 w-5" />
			{/if}
		</button>
	{/if}
</div>
