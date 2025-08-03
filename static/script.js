document.getElementById('speakBtn').addEventListener('click', () => {
    const text = document.getElementById('textInput').value.trim();
    if (!text) {
        alert('Please enter some text.');
        return;
    }

    fetch('/speak', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({text: text})
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