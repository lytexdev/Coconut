export async function getCsrfToken(): Promise<string> {
    const response = await fetch('/api/csrf-token');
    const data = await response.json();
    return data.csrf_token;
}
