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
    .then(res => res.json())
    .then(data => {
        if (data.audio_url) {
            document.getElementById('audio').src = data.audio_url;
        } else if (data.error) {
            alert('Error: ' + data.error);
        }
    })
    .catch(error => {
        alert('An error occurred: ' + error);
    });
});