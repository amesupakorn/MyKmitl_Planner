document.getElementById('start_date').addEventListener('change', function () {
    const selectedDateValue = this.value;  // วันที่ที่ผู้ใช้เลือกจาก input

    if (selectedDateValue) {
        document.getElementById('time_slots').classList.remove('hidden');
    } else {
        document.getElementById('time_slots').classList.add('hidden');
    }

    const facilityId = facility_id;  // สมมติว่าคุณมี facility_id ใน template ของคุณ

    const selectedDate = new Date(selectedDateValue);  // แปลง selectedDateValue เป็น Date object
    const currentDate = new Date();  // วันที่ปัจจุบัน
    const currentHours = currentDate.getHours();  // ชั่วโมงปัจจุบัน

    const timeButtons = document.querySelectorAll('button[data-time]');

    // 1. ตรวจสอบว่าผู้ใช้เลือกวันที่ในอดีตหรือไม่
    if (selectedDate < currentDate.setHours(0, 0, 0, 0)) {
        // ถ้าวันที่อยู่ในอดีต ให้ปิดการใช้งานปุ่มทั้งหมด
        timeButtons.forEach(button => {
            button.disabled = true;  // ปิดการใช้งานปุ่ม
            button.classList.remove('bg-orange-500', 'hover:bg-orange-600', 'text-white');
            button.classList.add('border-orange-500', 'cursor-not-allowed', 'border');  // เปลี่ยนสีและลักษณะปุ่ม
        });
        alert("ไม่สามารถจองวันที่ในอดีตได้!");  // แจ้งเตือนผู้ใช้
    }
    // 2. ตรวจสอบถ้าวันที่เลือกเป็นวันนี้
    else if (selectedDate.toDateString() === currentDate.toDateString()) {
        // ถ้าเป็นวันนี้ เปรียบเทียบชั่วโมงปัจจุบัน
        timeButtons.forEach(button => {
            const buttonHour = parseInt(button.getAttribute('data-time'), 10);  // ดึงชั่วโมงจาก data-time

            // ปิดการใช้งานปุ่มหากเวลาในปุ่มน้อยกว่าหรือเท่ากับชั่วโมงปัจจุบัน
            if (buttonHour <= currentHours) {
                button.disabled = true;  // ปิดการใช้งานปุ่ม
                button.classList.remove('bg-orange-500', 'hover:bg-orange-600', 'text-white');
                button.classList.add('border-orange-500', 'cursor-not-allowed', 'border');  // เปลี่ยนสีและลักษณะปุ่ม
            } else {
                button.disabled = false;  // เปิดใช้งานปุ่มสำหรับเวลาที่เหลือ
                button.classList.add('bg-orange-500', 'hover:bg-orange-600', 'text-white');
                button.classList.remove('border-orange-500', 'cursor-not-allowed', 'border', );  // เปลี่ยนสีและลักษณะปุ่ม
            }
        });
    }
    // 3. ถ้าเลือกวันที่ในอนาคต
    else {
        // ถ้าเป็นวันในอนาคต ให้เปิดการใช้งานปุ่มทั้งหมด
        timeButtons.forEach(button => {
            button.disabled = false;  // เปิดใช้งานปุ่ม
            button.classList.add('bg-orange-500', 'hover:bg-orange-600', 'text-white');
            button.classList.remove('border-orange-500', 'cursor-not-allowed', 'border', );  // เปลี่ยนสีและลักษณะปุ่ม
        });
    }
       
    // ส่ง request ไปที่ backend เพื่อดึงเวลา checkin ที่จองแล้ว
    fetch('check-available-times/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            date: selectedDateValue,
            facility_id: facilityId
        })
    })
    .then(response => response.json())
    .then(data => {

            data.forEach(bookedTime => {
                const timeButton = document.querySelector(`[data-time="${bookedTime.checkin_time}"]`);

                if (timeButton) {
                    timeButton.disabled = true; 
                    timeButton.classList.remove('bg-orange-500', 'hover:bg-orange-600', 'text-white');
                    timeButton.classList.add('border-orange-500', 'cursor-not-allowed', 'border'); 
                }
            });
        })
    .catch(error => console.error('Error fetching available times:', error));
});

// ทำให้ hover ค้างเมื่อคลิกปุ่ม
const timeButtons = document.querySelectorAll('#time_slots button');

timeButtons.forEach(button => {
    button.addEventListener('click', function () {

        // ลบเอฟเฟกต์ hover ค้างออกจากปุ่มทั้งหมดก่อน
        timeButtons.forEach(btn => {
            
            if(!btn.classList.contains('cursor-not-allowed')){
                btn.classList.remove('bg-orange-700');  // คลาสสำหรับ hover ค้าง
                btn.classList.add('bg-orange-500');  // คลาสปกติ
            }
        });

        // เพิ่มคลาสเพื่อให้เอฟเฟกต์ hover ค้างอยู่
        this.classList.remove('bg-orange-500', 'hover:bg-orange-600');
        this.classList.add('bg-orange-700');  // คลาสสำหรับสถานะที่เลือก

        selectedTime = this.getAttribute('data-time');
        document.getElementById('selected_time').value = selectedTime;
    });
});