<script>
	import { createEventDispatcher } from 'svelte';
	import { fade } from 'svelte/transition';

	const dispatch = createEventDispatcher();

	let uploadStatus = '';
	let isDragging = false;
	let fileInput;
	let preview = null;
	let uploadProgress = 0; // Add progress state
	let isUploading = false; // Add uploading state

	function handleDragEnter(e) {
		e.preventDefault();
		isDragging = true;
	}

	function handleDragLeave(e) {
		e.preventDefault();
		isDragging = false;
	}

	function handleDrop(e) {
		e.preventDefault();
		isDragging = false;
		const files = e.dataTransfer.files;
		if (files.length > 0) {
			fileInput.files = files;
			handleFileSelect(files[0]);
		}
	}

	function handleFileSelect(file) {
		if (file && file.type.startsWith('image/')) {
			preview = URL.createObjectURL(file);
		}
	}

	function handleFileInput(e) {
		const file = e.target.files[0];
		handleFileSelect(file);
	}

	async function handleSubmit(event) {
		const formData = new FormData(event.target);
		isUploading = true;
		uploadProgress = 0;

		try {
			const xhr = new XMLHttpRequest();

			xhr.upload.onprogress = (e) => {
				if (e.lengthComputable) {
					uploadProgress = Math.round((e.loaded / e.total) * 100);
				}
			};

			const uploadPromise = new Promise((resolve, reject) => {
				xhr.onload = () => {
					if (xhr.status === 200) {
						resolve(xhr.response);
					} else {
						reject(new Error('Upload failed'));
					}
				};
				xhr.onerror = () => reject(new Error('Upload failed'));

				xhr.open('POST', 'api/upload');
				xhr.send(formData);
			});

			await uploadPromise;

			uploadStatus = 'Image uploaded successfully!';
			preview = null;
			dispatch('uploadSuccess');
		} catch (error) {
			console.error('Error:', error);
			uploadStatus = 'An error occurred while uploading.';
		} finally {
			isUploading = false;
			uploadProgress = 0;
		}
	}
</script>

<div class="mx-auto my-8 max-w-xl">
	<form on:submit|preventDefault={handleSubmit} enctype="multipart/form-data" class="space-y-4">
		<!-- Drag & Drop Zone -->
		<div
			class="relative"
			on:dragenter|preventDefault={handleDragEnter}
			on:dragleave|preventDefault={handleDragLeave}
			on:dragover|preventDefault
			on:drop|preventDefault={handleDrop}
			role="region"
			aria-label="Image upload drop zone"
		>
			<input
				type="file"
				name="image"
				accept="image/*"
				required
				class="hidden"
				bind:this={fileInput}
				on:change={handleFileInput}
			/>
			<div
				class={`min-h-[200px] rounded-lg border-2 border-dashed p-4 text-center transition-all duration-200 ${
					isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
				} ${preview ? 'bg-gray-50' : 'bg-white'} cursor-pointer hover:border-blue-500 hover:bg-blue-50`}
				on:click={() => fileInput.click()}
				on:keydown={(e) => {
					if (e.key === 'Enter' || e.key === ' ') {
						e.preventDefault();
						fileInput.click();
					}
				}}
				role="button"
				tabindex="0"
				aria-label="Click or press Enter to select an image"
			>
				{#if preview}
					<div class="relative mx-auto aspect-video w-full max-w-md">
						<img
							src={preview}
							alt="Preview"
							class="h-full w-full rounded-lg object-contain"
							transition:fade
						/>
						<!-- Add this button -->
						<button
							type="button"
							class="absolute -right-2 -top-2 rounded-full bg-red-500 p-1 text-white
                   hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-500
                   focus:ring-offset-2"
							on:click|preventDefault={() => {
								preview = null;
								fileInput.value = '';
							}}
							aria-label="Remove image"
						>
							<svg
								xmlns="http://www.w3.org/2000/svg"
								class="h-5 w-5"
								viewBox="0 0 20 20"
								fill="currentColor"
							>
								<path
									fill-rule="evenodd"
									d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
									clip-rule="evenodd"
								/>
							</svg>
						</button>
					</div>
				{:else}
					<div class="flex h-full flex-col items-center justify-center space-y-2">
						<svg
							class="h-12 w-12 text-gray-400"
							fill="none"
							stroke="currentColor"
							viewBox="0 0 24 24"
							aria-hidden="true"
						>
							<path
								stroke-linecap="round"
								stroke-linejoin="round"
								stroke-width="2"
								d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
							></path>
						</svg>
						<p class="text-gray-600">Drag and drop your image here or click to select</p>
						<p class="text-sm text-gray-500">Supported formats: JPG, PNG, GIF</p>
					</div>
				{/if}
			</div>
		</div>

		<!-- Progress Bar -->
		{#if isUploading}
			<div class="w-full rounded-full bg-gray-200" transition:fade>
				<div
					class="rounded-full bg-blue-600 p-1 text-center text-xs font-medium leading-none text-white"
					style="width: {uploadProgress}%"
					transition:fade
				>
					{uploadProgress}%
				</div>
			</div>
		{/if}

		<!-- Upload Button -->
		<button
			type="submit"
			class="w-full rounded-lg bg-blue-600 px-4 py-2 text-white transition-colors
                   hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500
                   focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
			disabled={!preview || isUploading}
		>
			{#if isUploading}
				Uploading...
			{:else}
				Upload Image
			{/if}
		</button>

		<!-- Status Message -->
		{#if uploadStatus}
			<div
				class={`rounded-lg p-3 text-center ${
					uploadStatus.includes('successfully')
						? 'bg-green-100 text-green-700'
						: 'bg-red-100 text-red-700'
				}`}
				transition:fade
			>
				{uploadStatus}
			</div>
		{/if}
	</form>
</div>
