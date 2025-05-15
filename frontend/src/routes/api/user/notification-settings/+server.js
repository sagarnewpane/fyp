export async function GET({ fetch, cookies }) {
    const accessToken = cookies.get('access_token');

    if (!accessToken) {
        return new Response(JSON.stringify({ error: 'Not authenticated' }), {
            status: 401,
            headers: { 'Content-Type': 'application/json' }
        });
    }

    try {
        const response = await fetch('http://localhost:8000/api/user/notification-settings/', {
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        });

        const data = await response.json();
        return new Response(JSON.stringify(data), {
            status: response.status,
            headers: { 'Content-Type': 'application/json' }
        });

    } catch (error) {
        console.error('Failed to fetch notification settings:', error);
        return new Response(JSON.stringify({ error: 'Server error while fetching notification settings' }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' }
        });
    }
}

export async function PATCH({ request, fetch, cookies }) {
    const accessToken = cookies.get('access_token');

    if (!accessToken) {
        return new Response(JSON.stringify({ error: 'Not authenticated' }), {
            status: 401,
            headers: { 'Content-Type': 'application/json' }
        });
    }

    try {
        const settingsData = await request.json();
        const response = await fetch('http://localhost:8000/api/user/notification-settings/', {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(settingsData)
        });

        const data = await response.json();
        return new Response(JSON.stringify(data), {
            status: response.status,
            headers: { 'Content-Type': 'application/json' }
        });

    } catch (error) {
        console.error('Failed to update notification settings:', error);
        return new Response(JSON.stringify({ error: 'Server error while updating notification settings' }), {
            status: 500,
            headers: { 'Content-Type': 'application/json' }
        });
    }
} 