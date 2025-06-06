document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('storyForm');
    const viewBtn = document.getElementById('viewStory');
    form.addEventListener('submit', async (e) => {
        var _a;
        e.preventDefault();
        viewBtn.classList.add('hidden');
        const payload = {
            age: parseInt(document.getElementById('age').value, 10),
            interests: document.getElementById('interests').value,
            situation: document.getElementById('situation').value,
            guidance: document.getElementById('guidance').value
        };
        try {
            const res = await fetch('/story', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            if (!res.ok) {
                const err = await res.json();
                alert((_a = err.detail) !== null && _a !== void 0 ? _a : 'Error creating story');
                return;
            }
            const data = await res.json();
            const url = `/story/html/${data.scenario_id}`;
            viewBtn.onclick = () => window.open(url, '_blank');
            viewBtn.classList.remove('hidden');
            form.reset();
        }
        catch (err) {
            alert('Network error');
        }
    });
});
