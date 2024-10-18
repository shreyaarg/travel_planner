document.getElementById('itinerary-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = Object.fromEntries(formData.entries());

    const response = await fetch('/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    const result = await response.json();
    document.getElementById('itinerary-output').innerHTML = `
        <h2>Your Personalized Itinerary</h2>
        <pre>${JSON.stringify(result, null, 2)}</pre>
    `;
});
