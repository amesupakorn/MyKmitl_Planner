document.addEventListener('DOMContentLoaded', function() {
    const sendButton = document.getElementById('send-button');
    const messageInput = document.getElementById('message-input');
    const chatContainer = document.querySelector('.msger-chat');
    let userRole = '';
  
    const socket = new WebSocket('ws://localhost:8000/ws/messages/');
  
    // การจัดการการเชื่อมต่อ WebSocket
    socket.onopen = () => {
        console.log('Connected to WebSocket');
    };
  
    socket.onmessage = (e) => {
        const data = JSON.parse(e.data);
        displayNewMessage(data);  // แสดงข้อความที่ได้รับใน UI
    };
  
    socket.onclose = () => {
        console.log('Disconnected from WebSocket');
    };
  
    const loadMessages = () => {
        const welcomeMessage = {
          sender: 'staff',
          content: `สวัสดีครับ, ขอบคุณที่ส่งข้อความถึงเรา
          หากคุณมีปัญหาหรือข้อสงสัยอะไรโปรดกรอกรายละเอียดไว้ได้เลยครับ 
          เราจะพยายามตอบกลับถึงคุณโดยเร็วที่สุด`,
          timestamp: new Date()  // เวลา ณ ปัจจุบัน
        };
      
        displayNewMessage(welcomeMessage);  
  
        fetch('', {  // ระบุ URL ที่เหมาะสม
            method: 'GET',
            headers: {
                'Accept': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            userRole = data.user_role;
            data.messages.forEach(displayNewMessage); 
        })
        .catch((error) => {
            console.error('Error fetching messages:', error);
        });
    };
  
    const sendMessage = (content) => {
        const messageData = {
            content: content,
            sender: userRole,
        };
  
        socket.send(JSON.stringify(messageData));  // ส่งข้อความผ่าน WebSocket
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
            sendMessage(message);  // ส่งข้อความผ่าน WebSocket
            messageInput.value = '';  // ล้างช่องข้อความ
        }
    });
  
    messageInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendButton.click();
        }
    });
  
    loadMessages();
  });
  