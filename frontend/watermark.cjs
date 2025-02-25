const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function applyWatermark(inputPath, outputPath, settings) {
	const browser = await puppeteer.launch({
		headless: 'new',
		args: ['--no-sandbox', '--disable-setuid-sandbox']
	});

	try {
		const page = await browser.newPage();

		// Create HTML with fabric.js
		const html = `
        <!DOCTYPE html>
        <html>
        <head>
            <script src="https://cdnjs.cloudflare.com/ajax/libs/fabric.js/5.3.1/fabric.min.js"></script>
            <style>canvas { display: block; }</style>
        </head>
        <body>
            <canvas id="canvas"></canvas>
            <script>
                function getWatermarkPositions(width, height, settings) {
                    const positions = [];
                    const minDimension = Math.min(width, height);
                    const padding = minDimension * 0.05;
                    const spacing = Math.max((minDimension * settings.spacing) / 100, padding);

                    const offsetX = (width * settings.horizontalOffset) / 100;
                    const offsetY = (height * settings.verticalOffset) / 100;

                    const applyOffsets = (x, y) => ({
                        x: Math.min(Math.max(x + offsetX, padding), width - padding),
                        y: Math.min(Math.max(y + offsetY, padding), height - padding)
                    });

                    switch (settings.pattern) {
                        case 'single':
                            positions.push(applyOffsets(width / 2, height / 2));
                            break;

                        case 'diagonal':
                            const diagonalCount = 5;
                            for (let i = 0; i < diagonalCount; i++) {
                                positions.push(applyOffsets(
                                    padding + ((width - 2 * padding) * i) / (diagonalCount - 1),
                                    padding + ((height - 2 * padding) * i) / (diagonalCount - 1)
                                ));
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

                async function initCanvas(imageUrl, settings) {
                    return new Promise((resolve) => {
                        const canvas = new fabric.Canvas('canvas');

                        fabric.Image.fromURL(imageUrl, (img) => {
                            canvas.setDimensions({
                                width: img.width,
                                height: img.height
                            });

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

                            canvas.add(img);

                            const positions = getWatermarkPositions(img.width, img.height, settings);

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

                                canvas.add(watermark);
                                canvas.bringToFront(watermark);
                            });

                            canvas.renderAll();
                            resolve(canvas);
                        });
                    });
                }

                window.renderWatermark = async function(imageUrl, settings) {
                    const canvas = await initCanvas(imageUrl, settings);
                    return canvas.toDataURL('image/png');
                };
            </script>
        </body>
        </html>`;

		await page.setContent(html);

		// Convert input image to data URL
		const imageBuffer = fs.readFileSync(inputPath);
		const imageBase64 = `data:image/png;base64,${imageBuffer.toString('base64')}`;

		// Apply watermark
		const result = await page.evaluate(
			async (imageUrl, settings) => {
				return await window.renderWatermark(imageUrl, settings);
			},
			imageBase64,
			settings
		);

		// Save the result
		const outputBuffer = Buffer.from(result.split(',')[1], 'base64');
		fs.writeFileSync(outputPath, outputBuffer);

		return true;
	} catch (error) {
		console.error('Error applying watermark:', error);
		return false;
	} finally {
		await browser.close();
	}
}

// Handle command line arguments
const [, , inputPath, outputPath, settingsJson] = process.argv;

if (!inputPath || !outputPath || !settingsJson) {
	console.error('Missing required arguments');
	process.exit(1);
}

const settings = JSON.parse(settingsJson);

applyWatermark(inputPath, outputPath, settings)
	.then((success) => process.exit(success ? 0 : 1))
	.catch((error) => {
		console.error(error);
		process.exit(1);
	});
