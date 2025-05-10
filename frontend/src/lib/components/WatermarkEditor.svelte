<script>
	import { onMount, onDestroy } from 'svelte';
	import { fabric } from 'fabric';
	import { Eye, Plus, Minus, RotateCcw } from 'lucide-svelte';
	import { Button } from '$lib/components/ui/button';
	import { Input } from '$lib/components/ui/input';
	import { Card, CardContent, CardHeader, CardTitle } from '$lib/components/ui/card';
	import { Alert, AlertDescription } from '$lib/components/ui/alert';
	import * as Select from '$lib/components/ui/select';
	import { Slider } from '$lib/components/ui/slider';
	import { Tabs, TabsList, TabsTrigger, TabsContent } from '$lib/components/ui/tabs';
	import { toast } from 'svelte-sonner';
	import { Checkbox } from '$lib/components/ui/checkbox';
	import { Label } from '$lib/components/ui/label';

	export let imageUrl;
	export let initialSettings;
	export let imageId; // Make sure this prop is passed

	// Canvas state
	let canvas;
	let canvasElement;
	let watermarks = [];
	let backgroundImage = null;
	let isSaving = false;

	// Hidden Message
	let hiddenMessage = '';
	let fetchedMessage = 'No hidden message found'; // Default value
	let isStegApplied = false; // For the checkbox state

	// Fixed container dimensions
	const CONTAINER_WIDTH = 800;
	const CONTAINER_HEIGHT = 600;

	let currentZoom = 1;
	const ZOOM_STEP = 0.1;
	const MAX_ZOOM = 4;
	const MIN_ZOOM = 0.1;

	// Settings state
	let settings = initialSettings || {
		text: 'Watermark',
		font: 'Arial',
		color: '#000000',
		fontSize: 24,
		opacity: 50,
		rotation: 45,
		pattern: 'tiled',
		spacing: 50,
		horizontalOffset: 0,
		verticalOffset: 0
	};

	// Pattern options
	const patterns = [
		{ value: 'single', label: 'Single', description: 'Center watermark' },
		{ value: 'diagonal', label: 'Diagonal', description: 'Diagonal pattern' },
		{ value: 'grid', label: 'Grid', description: '3x3 grid layout' },
		{ value: 'corners', label: 'Corners', description: 'Corner watermarks' },
		{ value: 'tiled', label: 'Tiled', description: 'Full coverage' }
	];

	const fonts = ['Arial', 'Times New Roman', 'Georgia', 'Verdana', 'Courier New'];
	const fontOptions = fonts.map((font) => ({ value: font, label: font }));

	let selectedFont = {
		value: `${settings.font}`,
		label: settings.font.charAt(0).toUpperCase() + settings.font.slice(1).toLowerCase()
	};
	let selectedPattern = {
		value: `${settings.pattern}`,
		label: settings.pattern.charAt(0).toUpperCase() + settings.pattern.slice(1).toLowerCase()
	};

	function debounce(func, wait) {
		let timeout;
		return function executedFunction(...args) {
			const later = () => {
				clearTimeout(timeout);
				func(...args);
			};
			clearTimeout(timeout);
			timeout = setTimeout(later, wait);
		};
	}

	function handleResize() {
		if (!canvas || !backgroundImage) return;

		// Recalculate scale
		const scale = calculateImageScale(backgroundImage);

		// Center the image
		const left = (CONTAINER_WIDTH - backgroundImage.width * scale) / 2;
		const top = (CONTAINER_HEIGHT - backgroundImage.height * scale) / 2;

		// Update background image properties
		backgroundImage.set({
			scaleX: scale,
			scaleY: scale,
			left: left,
			top: top
		});

		// Update watermarks
		updateWatermarks();
		canvas.renderAll();
	}

	function initCanvas() {
		canvas = new fabric.Canvas(canvasElement, {
			backgroundColor: '#f3f4f6',
			preserveObjectStacking: true,
			width: CONTAINER_WIDTH,
			height: CONTAINER_HEIGHT
		});

		// Set the canvas container style
		const container = canvasElement.parentElement;
		container.style.width = `${CONTAINER_WIDTH}px`;
		container.style.height = `${CONTAINER_HEIGHT}px`;
		container.style.position = 'relative';

		canvas.renderAll();
	}

	function loadImageFromUrl(url) {
		if (!url) return;

		fabric.Image.fromURL(
			url,
			(img) => {
				canvas.clear();
				watermarks = [];
				currentZoom = 1;

				// Set canvas to EXACT original image dimensions
				const originalWidth = img.width;
				const originalHeight = img.height;

				canvas.setDimensions({
					width: originalWidth,
					height: originalHeight
				});

				// Set image at 1:1 scale
				img.set({
					left: 0,
					top: 0,
					originX: 'left',
					originY: 'top',
					selectable: false,
					evented: false,
					scaleX: 1,
					scaleY: 1
				});

				backgroundImage = img;
				canvas.add(backgroundImage);

				// Calculate initial zoom to fit in container
				const scaleX = CONTAINER_WIDTH / originalWidth;
				const scaleY = CONTAINER_HEIGHT / originalHeight;
				const initialZoom = Math.min(scaleX, scaleY, 1) * 0.9;
				currentZoom = initialZoom;
				canvas.setZoom(currentZoom);

				updateWatermarks();
				canvas.renderAll();
			},
			{ crossOrigin: 'anonymous' }
		);
	}

	function zoomIn() {
		if (currentZoom < MAX_ZOOM) {
			currentZoom = Math.min(currentZoom + ZOOM_STEP, MAX_ZOOM);
			canvas.setZoom(currentZoom);
			canvas.renderAll();
		}
	}

	function zoomOut() {
		if (currentZoom > MIN_ZOOM) {
			currentZoom = Math.max(currentZoom - ZOOM_STEP, MIN_ZOOM);
			canvas.setZoom(currentZoom);
			canvas.renderAll();
		}
	}

	function resetZoom() {
		const originalWidth = backgroundImage.width;
		const originalHeight = backgroundImage.height;
		const scaleX = CONTAINER_WIDTH / originalWidth;
		const scaleY = CONTAINER_HEIGHT / originalHeight;
		currentZoom = Math.min(scaleX, scaleY, 1) * 0.9;
		canvas.setZoom(currentZoom);
		canvas.renderAll();
	}

	function applyZoom() {
		if (!canvas || !backgroundImage) return;

		// Store current scroll position
		const container = canvasElement.parentElement.parentElement;
		const scrollLeft = container.scrollLeft;
		const scrollTop = container.scrollTop;

		// Calculate new dimensions
		const originalWidth = backgroundImage.width;
		const originalHeight = backgroundImage.height;
		const newWidth = originalWidth * currentZoom;
		const newHeight = originalHeight * currentZoom;

		// Update canvas size
		canvas.setDimensions({
			width: newWidth,
			height: newHeight
		});

		// Apply zoom to the entire canvas
		canvas.setZoom(currentZoom);
		canvas.renderAll();

		// Attempt to maintain scroll position
		container.scrollLeft = scrollLeft;
		container.scrollTop = scrollTop;
	}

	function getWatermarkPositions() {
		if (!canvas || !backgroundImage) return [];

		const positions = [];
		// Use the original image dimensions, without zoom
		const width = backgroundImage.width;
		const height = backgroundImage.height;
		const minDimension = Math.min(width, height);
		const padding = minDimension * 0.05;

		// Convert spacing percentage to actual pixels
		const spacing = Math.max((minDimension * settings.spacing) / 100, padding);

		// Calculate position offsets relative to image size
		const offsetX = (width * settings.horizontalOffset) / 100;
		const offsetY = (height * settings.verticalOffset) / 100;

		// Function to apply offsets and ensure positions are within image bounds
		const applyOffsets = (x, y) => {
			const newX = Math.min(Math.max(x + offsetX, padding), width - padding);
			const newY = Math.min(Math.max(y + offsetY, padding), height - padding);
			return { x: newX, y: newY };
		};

		switch (settings.pattern) {
			case 'single':
				positions.push(applyOffsets(width / 2, height / 2));
				break;

			case 'diagonal':
				const diagonalCount = 5;
				for (let i = 0; i < diagonalCount; i++) {
					positions.push(
						applyOffsets(
							padding + ((width - 2 * padding) * i) / (diagonalCount - 1),
							padding + ((height - 2 * padding) * i) / (diagonalCount - 1)
						)
					);
				}
				break;

			case 'grid':
				for (let x = padding; x < width - padding; x += spacing) {
					for (let y = padding; y < height - padding; y += spacing) {
						positions.push(applyOffsets(x, y));
					}
				}
				break;

			case 'corners':
				positions.push(
					applyOffsets(padding, padding),
					applyOffsets(width - padding, padding),
					applyOffsets(padding, height - padding),
					applyOffsets(width - padding, height - padding)
				);
				break;

			case 'tiled':
				const tileSpacing = spacing * 0.75;
				for (let x = padding; x < width - padding; x += tileSpacing) {
					for (let y = padding; y < height - padding; y += tileSpacing) {
						positions.push(applyOffsets(x, y));
					}
				}
				break;
		}

		return positions;
	}

	// function handleImageUpload(event) {
	// 	const file = event.target.files?.[0];
	// 	if (!file) return;

	// 	const reader = new FileReader();
	// 	reader.onload = (e) => {
	// 		const imgData = e.target.result;
	// 		fabric.Image.fromURL(imgData, (img) => {
	// 			canvas.clear();
	// 			watermarks = [];
	// 			currentZoom = 1; // Reset zoom when new image is loaded

	// 			// Set canvas dimensions to match the image dimensions
	// 			canvas.setDimensions({
	// 				width: img.width,
	// 				height: img.height
	// 			});

	// 			// Set image at its original size
	// 			img.set({
	// 				left: 0,
	// 				top: 0,
	// 				originX: 'left',
	// 				originY: 'top',
	// 				selectable: false,
	// 				evented: false,
	// 				scaleX: 1,
	// 				scaleY: 1
	// 			});

	// 			// Set background image and add to canvas
	// 			backgroundImage = img;
	// 			canvas.add(backgroundImage);

	// 			// Update watermarks after image is loaded
	// 			updateWatermarks();

	// 			canvas.renderAll();
	// 		});
	// 	};
	// 	reader.readAsDataURL(file);
	// }

	// Add wheel zoom support
	function handleWheel(event) {
		if (!event.ctrlKey) return; // Only zoom when Ctrl key is pressed

		event.preventDefault();

		const delta = event.deltaY;
		if (delta > 0) {
			zoomOut();
		} else {
			zoomIn();
		}
	}

	function calculateImageScale(img) {
		const containerRatio = CONTAINER_WIDTH / CONTAINER_HEIGHT;
		const imageRatio = img.width / img.height;

		if (imageRatio > containerRatio) {
			// Image is wider than container
			return (CONTAINER_WIDTH / img.width) * 0.9; // 0.9 to add some padding
		} else {
			// Image is taller than container
			return (CONTAINER_HEIGHT / img.height) * 0.9; // 0.9 to add some padding
		}
	}

	function updateWatermarks() {
		if (!canvas || !settings.text || !backgroundImage) return;

		// Remove existing watermarks
		watermarks.forEach((mark) => canvas.remove(mark));
		watermarks = [];

		const positions = getWatermarkPositions();

		// Create new watermarks
		positions.forEach((pos) => {
			const watermark = new fabric.Text(settings.text, {
				left: pos.x,
				top: pos.y,
				fontSize: settings.fontSize,
				fontFamily: settings.font,
				fill: settings.color,
				opacity: settings.opacity / 100,
				angle: settings.rotation,
				selectable: false,
				evented: false,
				originX: 'center',
				originY: 'center'
			});

			watermark.setCoords();
			watermarks.push(watermark);
			canvas.add(watermark);
			canvas.bringToFront(watermark);
		});

		canvas.requestRenderAll();
	}

	// function downloadImage() {
	// 	if (!canvas || !backgroundImage) return;

	// 	try {
	// 		// Store current zoom level
	// 		const currentZoomLevel = currentZoom;

	// 		// Temporarily reset zoom to 1 for export
	// 		currentZoom = 1;
	// 		canvas.setZoom(1);

	// 		// Set canvas to original dimensions
	// 		canvas.setDimensions({
	// 			width: backgroundImage.width,
	// 			height: backgroundImage.height
	// 		});

	// 		// Force re-render at original size
	// 		canvas.renderAll();

	// 		// Get data URL at original quality
	// 		const dataURL = canvas.toDataURL({
	// 			format: 'png',
	// 			quality: 1,
	// 			enableRetinaScaling: true
	// 		});

	// 		// Create and trigger download
	// 		const link = document.createElement('a');
	// 		link.download = 'watermarked-image.png';
	// 		link.href = dataURL;
	// 		link.click();

	// 		// Restore canvas state
	// 		currentZoom = currentZoomLevel;
	// 		canvas.setZoom(currentZoom);
	// 		canvas.setDimensions({
	// 			width: backgroundImage.width * currentZoom,
	// 			height: backgroundImage.height * currentZoom
	// 		});
	// 		canvas.renderAll();
	// 	} catch (error) {
	// 		console.error('Error during image download:', error);
	// 	}
	// }

	function resetCanvas() {
		if (!canvas) return;

		// Clear only watermarks without touching the background image
		watermarks.forEach((mark) => canvas.remove(mark));
		watermarks = [];

		// Reset settings to original values
		settings = {
			text: 'Your Watermark',
			font: 'Arial',
			color: '#000000',
			fontSize: 24,
			opacity: 50,
			rotation: 45,
			pattern: 'diagonal',
			spacing: 50,
			horizontalOffset: 0,
			verticalOffset: 0
		};

		// Reset select values
		selectedFont = { value: 'Arial', label: 'Arial' };
		selectedPattern = { value: 'diagonal', label: 'Diagonal' };

		// Update watermarks with new settings
		if (backgroundImage) {
			updateWatermarks();
		}

		canvas.renderAll();
	}

	async function fetchHiddenMessage() {
		try {
			const response = await fetch(`/api/hidden-message/${imageId}`);
			if (response.ok) {
				const data = await response.json();
				fetchedMessage = data.text || 'No hidden message found';
				isStegApplied = Boolean(data.text);
			} else {
				fetchedMessage = 'Failed to retrieve hidden message';
				isStegApplied = false;
			}
		} catch (error) {
			console.error('Error fetching hidden message:', error);
			fetchedMessage = 'Error retrieving hidden message';
			isStegApplied = false;
		}
	}

	async function saveHiddenMessage() {
		try {
			const method = isStegApplied ? 'PATCH' : 'POST';
			const response = await fetch(`/api/hidden-message/${imageId}`, {
				method,
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ text: hiddenMessage })
			});

			if (response.ok) {
				toast.success('Hidden message saved successfully');
				await fetchHiddenMessage(); // Refresh the displayed message
			} else {
				const error = await response.json();
				throw new Error(error.error || 'Failed to save hidden message');
			}
		} catch (error) {
			console.error('Error saving hidden message:', error);
			toast.error(error.message);
		}
	}

	async function deleteHiddenMessage() {
		try {
			const response = await fetch(`/api/hidden-message/${imageId}`, {
				method: 'DELETE'
			});

			if (response.ok) {
				toast.success('Hidden message removed successfully');
				hiddenMessage = '';
				fetchedMessage = 'No hidden message found';
				isStegApplied = false;
			} else {
				throw new Error('Failed to remove hidden message');
			}
		} catch (error) {
			console.error('Error deleting hidden message:', error);
			toast.error(error.message);
		}
	}

	async function saveWatermarkSettings() {
		if (!canvas || !backgroundImage) return;

		try {
			isSaving = true;
			const loadingToastId = toast.loading('Saving watermark settings...');

			const response = await fetch(`/api/image/${imageId}/watermark-settings/`, {
				method: 'PATCH',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					enabled: true,
					text: settings.text,
					font: settings.font,
					fontSize: settings.fontSize,
					color: settings.color,
					opacity: settings.opacity,
					rotation: settings.rotation,
					pattern: settings.pattern,
					spacing: settings.spacing,
					horizontalOffset: settings.horizontalOffset,
					verticalOffset: settings.verticalOffset
				})
			});

			if (!response.ok) {
				throw new Error('Failed to save watermark settings');
			}

			toast.dismiss(loadingToastId);
			toast.success('Watermark settings saved successfully');
		} catch (error) {
			console.error('Error saving watermark settings:', error);
			toast.error('Failed to save watermark settings. Please try again.');
		} finally {
			isSaving = false;
		}
	}

	onMount(() => {
		initCanvas();
		if (imageUrl) {
			loadImageFromUrl(imageUrl);
		}
		fetchHiddenMessage(); // Add this line
		return () => {
			if (canvas) {
				canvas.dispose();
			}
		};
	});

	// Watch for settings changes
	$: {
		if (canvas && backgroundImage) {
			const {
				pattern,
				font,
				spacing,
				horizontalOffset,
				verticalOffset,
				fontSize,
				opacity,
				rotation,
				color,
				text
			} = settings;
			updateWatermarks();
		}
	}

	$: {
		if (canvas && imageUrl) {
			loadImageFromUrl(imageUrl);
		}
	}
</script>

<div class="grid justify-center gap-6 lg:grid-cols-[1fr,500px]">
	<Card>
		<CardHeader class="pb-2">
			<CardTitle class="text-xl font-semibold">Image Watermarking Tool</CardTitle>
		</CardHeader>
		<CardContent class="p-4">
			<!-- Preview container with fixed size and scrollbars -->
			<div
				class="relative rounded-lg border bg-muted"
				style="width: {CONTAINER_WIDTH}px; height: {CONTAINER_HEIGHT}px;"
			>
				<!-- Zoom controls -->
				<div class="absolute left-4 top-4 z-10 flex gap-2">
					<Button variant="secondary" size="sm" on:click={zoomIn}>
						<Plus class="h-4 w-4" />
					</Button>
					<Button variant="secondary" size="sm" on:click={zoomOut}>
						<Minus class="h-4 w-4" />
					</Button>
					<Button variant="secondary" size="sm" on:click={resetZoom}>
						<RotateCcw class="h-4 w-4" />
					</Button>
					<span class="rounded bg-white/80 px-2 py-1 text-sm font-medium">
						{Math.round(currentZoom * 100)}%
					</span>
				</div>

				<!-- Scrollable container -->
				<div class="h-full w-full overflow-auto" on:wheel={handleWheel}>
					<div class="relative inline-block">
						<canvas bind:this={canvasElement}></canvas>
					</div>
				</div>
			</div>

			<!-- Zoom instructions -->
			<Alert class="mt-3">
				<AlertDescription>
					Use Ctrl + Mouse Wheel to zoom, or use the zoom controls above.
				</AlertDescription>
			</Alert>

			<!-- Existing alert -->
			<Alert class="mt-3 border-primary/20 bg-primary/5">
				<Eye class="h-4 w-4 text-primary" />
				<AlertDescription class="ml-2 text-sm">
					Watermark will be applied with {settings.opacity}% opacity in a {settings.pattern} pattern.
					Text will be rendered in {settings.font} at {settings.fontSize}px.
				</AlertDescription>
			</Alert>
		</CardContent>
	</Card>

	<Card>
		<CardHeader class="pb-2">
			<CardTitle class="text-xl font-semibold">Watermark Settings</CardTitle>
		</CardHeader>
		<CardContent class="space-y-4">
			<Tabs defaultValue="basic" class="w-full">
				<TabsList class="grid w-full grid-cols-3 border-b border-border">
					<TabsTrigger
						value="basic"
						class="data-[state=active]:border-b-2 data-[state=active]:border-primary"
					>
						Basic
					</TabsTrigger>
					<TabsTrigger
						value="advanced"
						class="data-[state=active]:border-b-2 data-[state=active]:border-primary"
					>
						Advanced
					</TabsTrigger>
					<TabsTrigger
						value="more-advanced"
						class="data-[state=active]:border-b-2 data-[state=active]:border-primary"
					>
						More Advanced
					</TabsTrigger>
				</TabsList>

				<TabsContent value="basic" class="space-y-4">
					<div class="mt-2 rounded-md border bg-muted p-4">
						<p class="mb-2 text-sm font-medium text-muted-foreground">Preview:</p>
						<div class="min-h-[60px] flex items-center justify-center">
							<p
								style="font-family: {settings.font}; font-size: {settings.fontSize}px; color: {settings.color}; opacity: {settings.opacity}%;"
								class="break-words text-center"
							>
								{settings.text || 'Your watermark text'}
							</p>
						</div>
					</div>
					<div class="space-y-2">
						<label for="watermark-text" class="text-sm font-medium">Text</label>
						<Input
							id="watermark-text"
							bind:value={settings.text}
							placeholder="Enter watermark text"
						/>
					</div>

					<div class="space-y-2">
						<label id="font-label" class="text-sm font-medium">Font</label>
						<Select.Root
							selected={selectedFont}
							onSelectedChange={(selected) => {
								if (selected) {
									selectedFont = selected;
									settings.font = selected.value;
									updateWatermarks();
								}
							}}
						>
							<Select.Trigger class="w-full">
								<Select.Value>
									<span style="font-family: {settings.font}">{settings.font}</span>
								</Select.Value>
							</Select.Trigger>
							<Select.Content>
								<Select.Group>
									{#each fontOptions as option}
										<Select.Item value={option.value} label={option.label}>
											<span style="font-family: {option.value}">{option.label}</span>
										</Select.Item>
									{/each}
								</Select.Group>
							</Select.Content>
						</Select.Root>
					</div>

					<div class="space-y-2">
						<label id="pattern-label" class="text-sm font-medium">Pattern</label>
						<Select.Root
							selected={selectedPattern}
							onSelectedChange={(selected) => {
								if (selected) {
									selectedPattern = selected;
									settings.pattern = selected.value;
									updateWatermarks();
								}
							}}
						>
							<Select.Trigger class="w-full">
								<Select.Value>
									{patterns.find((p) => p.value === settings.pattern)?.label || settings.pattern}
								</Select.Value>
							</Select.Trigger>
							<Select.Content>
								<Select.Group>
									{#each patterns as pattern}
										<Select.Item value={pattern.value} label={pattern.label}>
											{pattern.label}
											<span class="ml-2 text-sm text-muted-foreground">
												{pattern.description}
											</span>
										</Select.Item>
									{/each}
								</Select.Group>
							</Select.Content>
						</Select.Root>
					</div>
				</TabsContent>

				<TabsContent value="advanced" class="space-y-4">
					<!-- Image Preview -->
					<div class="mt-2 rounded-md border bg-muted p-4">
						<p class="mb-2 text-sm font-medium text-muted-foreground">Preview:</p>
						<div class="min-h-[60px] flex items-center justify-center">
							<p
								style="font-family: {settings.font}; font-size: {settings.fontSize}px; color: {settings.color}; opacity: {settings.opacity}%;"
								class="break-words text-center"
							>
								{settings.text || 'Your watermark text'}
							</p>
						</div>
					</div>

					<div class="space-y-2">
						<label for="font-size" class="text-sm font-medium">Size ({settings.fontSize}px)</label>
						<Slider
							id="font-size"
							value={[settings.fontSize]}
							onValueChange={([value]) => (settings.fontSize = value)}
							min={12}
							max={72}
							step={1}
						/>
					</div>

					<div class="space-y-2">
						<label for="opacity" class="text-sm font-medium">Opacity ({settings.opacity}%)</label>
						<Slider
							id="opacity"
							value={[settings.opacity]}
							onValueChange={([value]) => (settings.opacity = value)}
							min={0}
							max={100}
							step={1}
						/>
					</div>

					<div class="space-y-2">
						<label for="rotation" class="text-sm font-medium">Rotation ({settings.rotation}°)</label>
						<Slider
							id="rotation"
							value={[settings.rotation]}
							onValueChange={([value]) => (settings.rotation = value)}
							min={0}
							max={360}
							step={1}
						/>
					</div>

					<div class="space-y-2">
						<label for="spacing" class="text-sm font-medium">Spacing ({settings.spacing}%)</label>
						<Slider
							id="spacing"
							value={[settings.spacing]}
							onValueChange={([value]) => {
								settings.spacing = value;
								updateWatermarks();
							}}
							min={10}
							max={100}
							step={1}
						/>
					</div>

					<div class="space-y-2">
						<label for="horizontal-offset" class="text-sm font-medium">
							Horizontal Position ({settings.horizontalOffset}%)
						</label>
						<Slider
							id="horizontal-offset"
							value={[settings.horizontalOffset]}
							onValueChange={([value]) => {
								settings.horizontalOffset = value;
								updateWatermarks();
							}}
							min={-50}
							max={50}
							step={1}
						/>
					</div>

					<div class="space-y-2">
						<label for="vertical-offset" class="text-sm font-medium">
							Vertical Position ({settings.verticalOffset}%)
						</label>
						<Slider
							id="vertical-offset"
							value={[settings.verticalOffset]}
							onValueChange={([value]) => {
								settings.verticalOffset = value;
								updateWatermarks();
							}}
							min={-50}
							max={50}
							step={1}
						/>
					</div>
					<div class="space-y-2">
						<label for="color-picker" class="text-sm font-medium">Color</label>
						<div class="flex items-center gap-2">
							<div class="h-8 w-8 rounded border" style="background-color: {settings.color}"></div>
							<Input id="color-picker" type="color" bind:value={settings.color} class="h-8 w-12" />
							<Input type="text" bind:value={settings.color} class="flex-1" placeholder="#000000" />
						</div>
					</div>
				</TabsContent>

				<TabsContent value="more-advanced" class="space-y-4">
					<div class="space-y-4">
						<!-- Hidden Message Input -->
						<div class="space-y-2">
							<Label for="hidden-message" class="text-sm font-medium">Hidden Message</Label>
							<Input
								id="hidden-message"
								bind:value={hiddenMessage}
								placeholder="Enter message to hide in image"
							/>
						</div>

						<!-- Fetched Message Display -->
						<div class="space-y-2">
							<Label class="text-sm font-medium">Retrieved Hidden Message</Label>
							<div class="rounded-md border bg-muted p-3">
								<p class="text-sm text-muted-foreground">{fetchedMessage}</p>
							</div>
						</div>

						<!-- Applied Status -->
						<div class="flex items-center space-x-2">
							<Checkbox id="applied" checked={isStegApplied} disabled={true} />
							<Label
								for="applied"
								class="text-sm font-medium leading-none peer-disabled:cursor-not-allowed peer-disabled:opacity-70"
							>
								Steganography Applied
							</Label>
						</div>

						<!-- Information Alert -->
						<Alert>
							<AlertDescription>
								Steganography allows you to hide messages within your image that won't be visible to
								the naked eye. The message will be securely embedded in the image data.
							</AlertDescription>
						</Alert>
					</div>

					<div class="space-y-2 pt-2">
						<Button class="w-full" on:click={saveHiddenMessage} disabled={!hiddenMessage}>
							{isStegApplied ? 'Update' : 'Save'} Hidden Message
						</Button>

						{#if isStegApplied}
							<Button variant="destructive" class="w-full" on:click={deleteHiddenMessage}>
								Remove Hidden Message
							</Button>
						{/if}
					</div>
				</TabsContent>
			</Tabs>

			<div class="sticky bottom-0 space-y-2 bg-background pt-4">
				<Button class="w-full" on:click={saveWatermarkSettings} disabled={isSaving}>
					{#if isSaving}
						Saving Settings...
					{:else}
						Save Settings
					{/if}
				</Button>

				<Button variant="outline" class="w-full" on:click={resetCanvas} disabled={isSaving}>
					Reset Settings
				</Button>
			</div>
		</CardContent>
	</Card>
</div>

<style>
	/* Add these styles to your component */
	.overflow-auto {
		overflow: auto;
		scrollbar-width: thin;
		scrollbar-color: rgba(0, 0, 0, 0.2) transparent;
	}

	.overflow-auto::-webkit-scrollbar {
		width: 8px;
		height: 8px;
	}

	.overflow-auto::-webkit-scrollbar-track {
		background: transparent;
	}

	.overflow-auto::-webkit-scrollbar-thumb {
		background-color: rgba(0, 0, 0, 0.2);
		border-radius: 4px;
	}

	.overflow-auto::-webkit-scrollbar-thumb:hover {
		background-color: rgba(0, 0, 0, 0.3);
	}
</style>
