let messages = [
    { role: 'system', content: 'As a helpful assistant, you will write clean, well-organized, and easy-to-understand front-end code. The code should be written in json format. The key is the filename and the value is the content of the file.' }
];

async function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    if (!userInput.trim()) return;

    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML += `<div><strong>You:</strong> ${userInput}</div>`;

    messages.push({ role: 'user', content: userInput });

    document.getElementById('loading').style.display = 'flex';

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ messages })
        });

        const data = await response.json();
        messages = data.response;

        const link = document.createElement('a');
        link.href = `/${data.path}/index.html`;
        link.textContent = 'View Generated Files';
        link.target = '_blank';
        chatBox.appendChild(link);

        document.getElementById('user-input').value = '';
    } catch (error) {
        console.error('Error:', error);
    } finally {
        document.getElementById('loading').style.display = 'none';
    }
}
