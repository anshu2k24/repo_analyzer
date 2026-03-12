const API_BASE_URL = 'http://localhost:8000';

document.addEventListener('DOMContentLoaded', () => {
    const ingestForm = document.getElementById('ingest-form');
    const repoUrlInput = document.getElementById('repo-url');
    const ingestBtn = document.getElementById('ingest-btn');
    const ingestStatus = document.getElementById('ingest-status');
    const currentRepoDisplay = document.getElementById('current-repo-display');
    const chatForm = document.getElementById('chat-form');
    const questionInput = document.getElementById('question-input');
    const sendBtn = document.getElementById('send-btn');
    const chatMessages = document.getElementById('chat-messages');

    // Handle initial state
    let isRepoIngested = false;

    // Auto-resize textarea
    questionInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
        
        // Enable/disable send button based on content
        if (this.value.trim() && isRepoIngested) {
            sendBtn.disabled = false;
        } else {
            sendBtn.disabled = true;
        }
    });

    // Handle enter key to submit
    questionInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!sendBtn.disabled) {
                chatForm.dispatchEvent(new Event('submit'));
            }
        }
    });

    // Handle Ingestion
    ingestForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const repoUrl = repoUrlInput.value.trim();
        
        if (!repoUrl) return;

        // UI updates for loading
        ingestBtn.disabled = true;
        ingestBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i><span>Ingesting...</span>';
        ingestStatus.className = 'loading';
        ingestStatus.textContent = 'Cloning and embedding codebase. This may take a few minutes...';
        
        try {
            const response = await fetch(`${API_BASE_URL}/ingest`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ repo_url: repoUrl }),
            });

            const data = await response.json();

            if (response.ok) {
                ingestStatus.className = 'success';
                ingestStatus.innerHTML = `<i class="fa-solid fa-check-circle"></i> ${data.message}`;
                
                // Extract repo name for display
                const repoParts = repoUrl.split('/');
                const repoName = repoParts[repoParts.length - 1].replace('.git', '');
                currentRepoDisplay.textContent = repoName;
                
                // Enable chat
                isRepoIngested = true;
                questionInput.disabled = false;
                questionInput.placeholder = `Ask a question about ${repoName}...`;
                
                // Remove welcome message if exists
                const welcomeMsg = document.querySelector('.welcome-message');
                if (welcomeMsg) {
                    welcomeMsg.style.display = 'none';
                }
            } else {
                throw new Error(data.detail || 'Failed to ingest repository');
            }
        } catch (error) {
            ingestStatus.className = 'error';
            ingestStatus.innerHTML = `<i class="fa-solid fa-triangle-exclamation"></i> ${error.message}`;
        } finally {
            ingestBtn.disabled = false;
            ingestBtn.innerHTML = '<span>Ingest Codebase</span><i class="fa-solid fa-arrow-right"></i>';
        }
    });

    // Handle Chat
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const question = questionInput.value.trim();
        
        if (!question || !isRepoIngested) return;

        // 1. Add user message to chat
        addMessage(question, 'user');
        
        // Clear input
        questionInput.value = '';
        questionInput.style.height = 'auto';
        sendBtn.disabled = true;
        
        // 2. Show typing indicator
        const typingId = showTypingIndicator();
        
        // 3. Send to API
        try {
            const response = await fetch(`${API_BASE_URL}/ask`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: question, repo_name: currentRepoDisplay.textContent }),
            });

            removeTypingIndicator(typingId);

            if (response.ok) {
                // Prepare message bubble
                const msgId = 'bot-msg-' + Date.now();
                const msgDiv = document.createElement('div');
                msgDiv.className = 'message bot';
                msgDiv.id = msgId;
                chatMessages.appendChild(msgDiv);
                scrollToBottom();

                const reader = response.body.getReader();
                const decoder = new TextDecoder('utf-8');
                let fullText = '';

                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;
                    
                    const chunk = decoder.decode(value, { stream: true });
                    fullText += chunk;
                    msgDiv.innerHTML = escapeHtmlAndFormatCode(fullText);
                    scrollToBottom();
                }
            } else {
                const data = await response.json();
                throw new Error(data.detail || 'Failed to get answer');
            }
        } catch (error) {
            removeTypingIndicator(typingId);
            addMessage(`Error: ${error.message}`, 'bot');
        }
    });

    function addMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${sender}`;
        
        if (sender === 'bot') {
            msgDiv.innerHTML = text; // Allow HTML for formatted response
        } else {
            msgDiv.textContent = text;
        }
        
        chatMessages.appendChild(msgDiv);
        scrollToBottom();
    }

    function showTypingIndicator() {
        const id = 'typing-' + Date.now();
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.id = id;
        
        for (let i = 0; i < 3; i++) {
            const dot = document.createElement('div');
            dot.className = 'typing-dot';
            typingDiv.appendChild(dot);
        }
        
        chatMessages.appendChild(typingDiv);
        scrollToBottom();
        return id;
    }

    function removeTypingIndicator(id) {
        const element = document.getElementById(id);
        if (element) {
            element.remove();
        }
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Very basic markdown parsing for code blocks
    function escapeHtmlAndFormatCode(text) {
        if (!text) return '';
        
        // Replace HTML tags to prevent XSS (basic)
        let escaped = text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");

        // Format code blocks (```code```)
        escaped = escaped.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
        
        // Format inline code (`code`)
        escaped = escaped.replace(/`([^`]+)`/g, '<code>$1</code>');
        
        // Format bold (**text**)
        escaped = escaped.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
        
        return escaped;
    }
});
