import { error } from '@sveltejs/kit';

// Define the backend base URL.
// In a production app, you'd likely use an environment variable for this.
const BACKEND_BASE_URL = 'http://localhost:8000'; // Ensure this matches your Django backend URL

export async function GET({ params, fetch }) {
    const { token } = params;

    if (!token) {
        throw error(400, 'Access token is required');
    }

    // Construct the URL to your new Django backend endpoint
    const backendUrl = `${BACKEND_BASE_URL}/api/access/${token}/download-protected/`;

    try {
        const backendResponse = await fetch(backendUrl,{
            method: 'GET'
        });

        if (!backendResponse.ok) {
            let errorBody = 'Failed to download protected image from backend.';
            try {
                const backendError = await backendResponse.json();
                errorBody = backendError.error || backendError.detail || errorBody;
            } catch (e) {
                // Could not parse JSON, use default error or statusText
                errorBody = backendResponse.statusText || errorBody;
            }
            console.error(`Backend request failed: ${backendResponse.status} ${errorBody}`);
            throw error(backendResponse.status, errorBody);
        }

        const contentType = backendResponse.headers.get('content-type') || 'application/octet-stream';
        const contentDisposition = backendResponse.headers.get('content-disposition');

        const headers = {
            'Content-Type': contentType,
            // Ensure no caching for sensitive images that might change or be revoked
            'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0'
        };

        if (contentDisposition) {
            headers['Content-Disposition'] = contentDisposition;
        }

        return new Response(backendResponse.body, {
            status: backendResponse.status,
            statusText: backendResponse.statusText,
            headers: headers
        });

    } catch (e) {
        console.error('Error proxying protected image download request:', e);
        if (e.status) { // If it's a SvelteKit error (thrown by error())
            throw e;
        }
        throw error(500, 'Internal server error while downloading protected image.');
    }
} 