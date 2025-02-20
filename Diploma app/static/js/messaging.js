class MessagingSystem {
    constructor() {
        this.messages = [];
        this.currentChat = null;
    }

    initializeChat(patientId) {
        this.currentChat = patientId;
        this.loadMessages(patientId);
        this.setupMessageListener();
    }

    loadMessages(patientId) {
        fetch(`/get_messages/${patientId}`)
            .then(response => response.json())
            .then(messages => {
                this.displayMessages(messages);
            });
    }

    sendMessage(message) {
        if (!this.currentChat) return;

        fetch('/send_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                patientId: this.currentChat,
                message: message
            })
        })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                this.appendMessage({
                    sender: 'doctor',
                    content: message,
                    timestamp: new Date()
                });
            }
        });
    }

    displayMessages(messages) {
        const chatContainer = document.querySelector('.chat-messages');
        chatContainer.innerHTML = messages.map(msg => `
            <div class="message ${msg.sender}">
                <div class="message-content">${msg.content}</div>
                <div class="message-timestamp">${new Date(msg.timestamp).toLocaleTimeString()}</div>
            </div>
        `).join('');
    }

    setupMessageListener() {
        // Set up WebSocket or polling for real-time messages
    }
} 