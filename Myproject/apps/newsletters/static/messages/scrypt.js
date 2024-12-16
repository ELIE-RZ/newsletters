
    const form = document.getElementById('send-message-form');
    const messageList = document.getElementById('message-list');
    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const content = document.getElementById('message-content').value;
        const receiverId = form.querySelector('input[name="receiver_id"]').value;

        const response = await fetch("{% url 'send_message' %}", {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': '{{ csrf_token }}'
            },
            body: JSON.stringify({ content, receiver_id: receiverId })
        });

        const data = await response.json();
        if (data.status === 'success') {
            const newMessage = document.createElement('div');
            newMessage.classList.add('message', 'sent');
            newMessage.innerHTML = `<p><strong>Vous:</strong> ${content}</p><small>Just now</small>`;
            messageList.appendChild(newMessage);
            form.reset();
        }
    });
