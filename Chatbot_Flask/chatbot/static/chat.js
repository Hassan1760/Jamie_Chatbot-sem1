document.addEventListener('DOMContentLoaded', function(){
    const msgInput = document.getElementById('message-input');
    const sendBtn = document.getElementById('send-btn');
    const messagesContainer = document.getElementById('messages-container');

    // Send message on button click
    sendBtn.addEventListener('click', sendMessage);

    // Send message on Enter key
    msgInput.addEventListener('keypress', e => {
        if(e.key === 'Enter') sendMessage();
    });

    function sendMessage(){
        const text = msgInput.value.trim();
        if(!text) return;

        // Show user message
        addMessage(text, 'user');

        msgInput.value = '';

        // Send message to Flask backend
        fetch('/get', {
            method:'POST',
            headers:{'Content-Type':'application/x-www-form-urlencoded'},
            body:'msg='+encodeURIComponent(text)
        })
        .then(res => res.json())
        .then(data => addMessage(data.response, 'bot'))
        .catch(() => addMessage('Server error!', 'bot'));
    }

    function addMessage(text, sender){
        const div = document.createElement('div');
        div.className = `message ${sender}-message`;

        const content = document.createElement('div');
        content.className = 'message-content';

        // Replace \n with <br> so new lines appear in chat
        content.innerHTML = text.replace(/\n/g, '<br>');

        div.appendChild(content);
        messagesContainer.appendChild(div);

        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // Optional: handle quick replies
    document.addEventListener('click', function(e){
        if(e.target.classList.contains('quick-reply')){
            const reply = e.target.getAttribute('data-reply');
            msgInput.value = reply;
            sendMessage();
        }
    });
});
