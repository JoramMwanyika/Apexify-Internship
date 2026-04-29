document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const typingTemplate = document.getElementById('typing-template');

    // Focus input on load
    userInput.focus();

    // Event Listeners
    sendBtn.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    async function sendMessage() {
        const text = userInput.value.trim();
        if (!text) return;

        // 1. Append User Message
        appendMessage(text, 'user');
        userInput.value = '';

        // 2. Show Typing Indicator
        showTypingIndicator();

        try {
            // 3. Send request to backend
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text })
            });

            const data = await response.json();

            // 4. Remove Typing Indicator and Show Bot Response
            // Added a small simulated delay to make it feel natural
            setTimeout(() => {
                removeTypingIndicator();
                appendMessage(data.response, 'bot', data.intent);
            }, 600);

        } catch (error) {
            console.error('Error fetching chat response:', error);
            removeTypingIndicator();
            appendMessage("Sorry, I'm having trouble connecting to the server.", 'bot', 'ERROR');
        }
    }

    function appendMessage(text, sender, intent = null) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}-message`;

        let contentHtml = '';

        // Only add intent badge for bot messages
        if (sender === 'bot' && intent) {
            contentHtml += `<div class="intent-badge">[Intent: ${intent}]</div>`;
        }

        contentHtml += `
            <div class="message-content">
                <p>${text}</p>
            </div>
        `;

        msgDiv.innerHTML = contentHtml;
        chatBox.appendChild(msgDiv);
        scrollToBottom();
    }

    function showTypingIndicator() {
        const clone = typingTemplate.content.cloneNode(true);
        chatBox.appendChild(clone);
        scrollToBottom();
    }

    function removeTypingIndicator() {
        const indicator = document.getElementById('typing-indicator');
        if (indicator) {
            indicator.remove();
        }
    }

    function scrollToBottom() {
        chatBox.scrollTop = chatBox.scrollHeight;
    }
});
