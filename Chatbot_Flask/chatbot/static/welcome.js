document.addEventListener('DOMContentLoaded', function() {
    const startChatBtn = document.getElementById('startChatBtn');
    const funTextElement = document.querySelector('.fun-text');

    startChatBtn.addEventListener('click', startChat);

    function startChat() {
        if (startChatBtn.disabled) return; // prevent multiple clicks

        startChatBtn.disabled = true;
        startChatBtn.classList.add('loading');
        startChatBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Connecting...';

        // Robo elements
        const roboMouth = document.querySelector('.robo-mouth');
        const pupils = document.querySelectorAll('.eye-pupil');
        const leftArm = document.querySelector('.left-arm');
        const rightArm = document.querySelector('.right-arm');

        // Mouth animation
        if (roboMouth) roboMouth.style.backgroundColor = '#4cd964';

        // Eye pupils animation
        pupils.forEach(p => p.style.backgroundColor = '#4cd964');

        // Arms waving
        if(leftArm && rightArm){
            leftArm.style.transform = 'rotate(60deg)';
            rightArm.style.transform = 'rotate(-60deg)';
        }

        // Fun loading messages
        const messages = [
            "🤖 Initializing Robo...",
            "📡 Establishing connection...",
            "💭 Loading module...",
            "🎯 Almost ready..."
        ];
        let index = 0;

        const msgInterval = setInterval(() => {
            if(index < messages.length){
                funTextElement.textContent = messages[index++];
                funTextElement.style.color = '#6a5af9';
            } else {
                clearInterval(msgInterval);
            }
        }, 600);

        // Complete loading + redirect
        setTimeout(() => {
            startChatBtn.innerHTML = '<i class="fas fa-check"></i> Connected!';
            startChatBtn.style.background = 'linear-gradient(to right, #4cd964, #2ecc71)';
            funTextElement.textContent = "✅ Redirecting to chat...";
            funTextElement.style.color = '#2ecc71';

            setTimeout(() => {
                window.location.href = 'main'; // redirect to main.html
            }, 800);
        }, 2500);
    }

    // Eyes follow cursor
    document.addEventListener('mousemove', function(e){
        const roboHead = document.querySelector('.robo-head');
        const pupils = document.querySelectorAll('.eye-pupil');

        if(roboHead && pupils.length > 0){
            const headRect = roboHead.getBoundingClientRect();
            const centerX = headRect.left + headRect.width / 2;
            const centerY = headRect.top + headRect.height / 2;

            const moveX = (e.clientX - centerX) / 50;
            const moveY = (e.clientY - centerY) / 50;

            pupils.forEach(pupil => {
                pupil.style.transform = `translate(calc(-50% + ${moveX}px), calc(-50% + ${moveY}px))`;
            });
        }
    });
});

