import { json } from '@sveltejs/kit';

export async function POST({ request, cookies }) {
    const accessToken = cookies.get('access_token');

    if (!accessToken) {
        return json({ error: 'Not authenticated' }, { status: 401 });
    }

    try {
        const body = await request.json();
        const response = await fetch('http://localhost:8000/api/delete-account/', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(body)
        });

        const data = await response.json();
        return json(data, { status: response.status });
    } catch (error) {
        console.error('Error deleting account:', error);
        return json({ error: 'Failed to delete account' }, { status: 500 });
    }
} 