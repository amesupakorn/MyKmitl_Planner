document.addEventListener('DOMContentLoaded', function() {
  const sendButton = document.getElementById('send-button');
  const messageInput = document.getElementById('message-input');
  const chatContainer = document.querySelector('.msger-chat');
  let = userRole = '';

  const loadMessages = () => {
      const welcomeMessage = {
        student: 0,  // ใช้ 0 เพื่อบ่งบอกว่าเป็นข้อความจากเจ้าหน้าที่
        content: `สวัสดีครับ, ขอบคุณที่ส่งข้อความถึงเรา
        หากคุณมีปัญหาหรือข้อสงสัยอะไรโปรดกรอกรายละเอียดไว้ได้เลยครับ 
        เราจะพยายามตอบกลับถึงคุณโดยเร็วที่สุด`,
        timestamp: new Date()  // เวลา ณ ปัจจุบัน
      };
    
    displayNewMessage(welcomeMessage);  

    fetch('', {  
        method: 'GET',
        headers: {
            'Accept': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        userRole = data.user_role
        data.messages.forEach(displayNewMessage); 
    })
    .catch((error) => {
        console.error('Error fetching messages:', error);
    });
  };

  const sendMessage = (content) => {
        const messageData = {
          content: content,
          status: "sent",
          sender: userRole,
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
    
    const isStudentMessage = message.sender === 'student';  

    const messageElement = document.createElement('div');
    messageElement.classList.add('msg', isStudentMessage ? 'right-msg' : 'left-msg');  
    messageElement.innerHTML = `
          <div class="msg-bubble">
              <div class="msg-info">
                  <div class="msg-info-name">${isStudentMessage ? 'You' : 'Staff'}</div>
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
