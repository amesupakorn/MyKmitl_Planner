document.addEventListener('DOMContentLoaded', function() {
    const sendButton = document.getElementById('send-button');
    const messageInput = document.getElementById('message-input');
    const chatContainer = document.querySelector('.msger-chat');
    let userRole = '';
    let studentId = '';
    let studentName = '';
    // Function to send message to API
  
    const loadMessages = () => {  
      fetch('', {  
          method: 'GET',
          headers: {
              'Accept': 'application/json',
          },
      })
      .then(response =>{
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
      .then(data => {
            userRole = data.user_role;
            studentId = data.studentId;
            studentName = data.student_name;

            data.messages.forEach(displayNewMessage);
      })
      .catch((error) => {
            console.error('Error fetching messages:', error);
      });
    };
  
    const sendMessage = (content) => {
          const messageData = {
            content: content,
            status: "delivered",
            sender: userRole
        };
  
        fetch('', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
  
            },
            body: JSON.stringify(messageData),
        })
        .then(response => response.json())
        .then(data => {
          displayNewMessage(data); 
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    };
  
    // Function to display new message in UI
    const displayNewMessage = (message) => {
      const isStaffMessage = message.sender === 'staff';  

      const messageElement = document.createElement('div');
      messageElement.classList.add('msg', isStaffMessage ? 'right-msg' : 'left-msg');  
      messageElement.innerHTML = `
            <div class="msg-bubble">
                <div class="msg-info">
                    <div class="msg-info-name">${isStaffMessage ? 'You' : studentName}</div>
                    <div class="msg-info-time">
                            ${new Date(message.timestamp).toLocaleDateString()} ${new Date(message.timestamp).toLocaleTimeString()}

                    </div>
                </div>
                <div class="msg-text">
                    ${message.content}
                </div>
            </div>
        `;
        
        chatContainer.appendChild(messageElement);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    };
  
    sendButton.addEventListener('click', () => {
        const message = messageInput.value;
        if (message.trim() !== "") {
            sendMessage(message);  
            messageInput.value = '';  
        }
    });
  
    messageInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendButton.click();
        }
    });
  
    loadMessages();
  });
  