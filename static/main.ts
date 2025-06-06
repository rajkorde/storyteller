interface StoryRequest {
  age: number;
  interests: string;
  situation: string;
  guidance?: string;
}

document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('storyForm') as HTMLFormElement;
  const viewBtn = document.getElementById('viewStory') as HTMLButtonElement;

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    viewBtn.classList.add('hidden');

    const payload: StoryRequest = {
      age: parseInt((document.getElementById('age') as HTMLInputElement).value, 10),
      interests: (document.getElementById('interests') as HTMLInputElement).value,
      situation: (document.getElementById('situation') as HTMLTextAreaElement).value,
      guidance: (document.getElementById('guidance') as HTMLInputElement).value
    };

    try {
      const res = await fetch('/story', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      if (!res.ok) {
        const err = await res.json();
        alert(err.detail ?? 'Error creating story');
        return;
      }

      const data = await res.json();
      const url = `/story/html/${data.scenario_id}`;
      viewBtn.onclick = () => window.open(url, '_blank');
      viewBtn.classList.remove('hidden');
      form.reset();
    } catch (err) {
      alert('Network error');
    }
  });
});
