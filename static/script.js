document.getElementById('speakBtn').addEventListener('click', () => {
    const text = document.getElementById('textInput').value.trim();
    if (!text) {
        alert('Please enter some text.');
        return;
    }

    const formData = new FormData();
    formData.append('text', text);
    
    fetch('/tts', {
        method: 'POST',
        body: formData
    })
    .then(res => {
        if (!res.ok) {
            throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
    })
    .then(data => {
        console.log('TTS Response:', data);
        if (data.audio_url) {
            const audioElement = document.getElementById('audio');
            audioElement.src = data.audio_url;
            audioElement.style.display = 'block';
            
            // Try to play the audio
            audioElement.play().catch(e => {
                console.log('Auto-play prevented by browser:', e);
            });
            
            if (data.message) {
                console.log('TTS Message:', data.message);
            }
        } else if (data.error) {
            alert('Error: ' + data.error);
        } else {
            alert('Unexpected response format');
        }
    })
    .catch(error => {
        console.error('TTS Error:', error);
        alert('An error occurred: ' + error.message);
    });
});