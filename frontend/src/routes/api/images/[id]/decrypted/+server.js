import { error } from '@sveltejs/kit';

// Define the backend base URL. 
// In a production app, you'd likely use an environment variable for this.
const BACKEND_BASE_URL = 'http://localhost:8000';

export async function GET({ params, fetch: svelteKitFetch }) {
    const { id } = params;

    if (!id) {
        throw error(400, 'Image ID is required');
    }

    const backendUrl = `${BACKEND_BASE_URL}/images/${id}/decrypted/`;

    try {
        // Use SvelteKit's fetch for server-side requests to handle cookies/credentials if needed
        // and to enable relative paths if your backend was on the same domain (not the case here).
        const backendResponse = await svelteKitFetch(backendUrl);

        if (!backendResponse.ok) {
            // Forward the error status and a generic message from the backend if possible
            console.error(`Backend request failed: ${backendResponse.status} ${backendResponse.statusText}`);
            const errorBody = await backendResponse.text(); // Attempt to get error body
            throw error(backendResponse.status, `Failed to fetch image from backend: ${errorBody || backendResponse.statusText}`);
        }

        // Get the content type from the backend response
        const contentType = backendResponse.headers.get('content-type') || 'application/octet-stream';

        // Stream the backend response body back to the client
        return new Response(backendResponse.body, {
            status: backendResponse.status,
            statusText: backendResponse.statusText,
            headers: {
                'Content-Type': contentType,
                // You might want to add Content-Disposition if your backend sends it
                // and you want to suggest a filename to the browser for this proxied request.
                // 'Content-Disposition': backendResponse.headers.get('content-disposition') || `attachment; filename="decrypted_image_${id}.png"`,
                'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0' // Ensure no caching for sensitive images
            }
        });

    } catch (e) {
        console.error('Error proxying decrypted image request:', e);
        // If it's already a SvelteKit error, re-throw it
        if (e.status) {
            throw e;
        }
        // Otherwise, throw a generic 500 error
        throw error(500, 'Internal server error while fetching image');
    }
}
