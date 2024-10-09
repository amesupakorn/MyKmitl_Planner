
function deleteFacility(facilityId) {
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'Cancel'
    }).then((result) => {
        if (result.isConfirmed) {
            // หากผู้ใช้ยืนยันการลบ, ทำการลบด้วย fetch()
            fetch('', {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    facility_id: facilityId
                })
            })
            .then(response => {
                if (response.ok) {
                    window.location.href = '/booking/facilities/';  
                }
            })
            .catch(error => {
                console.error('Error:', error);
                Swal.fire('Error!', 'Something went wrong.', 'error');
            });
        }
    });
}


// ฟังก์ชันล้างฟอร์ม
function clearForm() {
    document.getElementById('editfacilityForm').reset();
}

// เมื่อกดปุ่ม Edit ให้ดึงข้อมูลจาก backend
document.querySelectorAll('.edit-btn').forEach(button => {
    button.addEventListener('click', function() {
        const facilityId = this.getAttribute('data-id');  // ดึง facility_id จากปุ่ม
        fetch(`edit/${facilityId}`)  // เรียก GET ไปยัง API ที่สร้างใน views.py
            .then(response => response.json())
            .then(data => {
                // เปิด modal
                document.getElementById('editfacilityModal').classList.remove('hidden');
                
                // เติมข้อมูลลงในฟอร์ม
                document.getElementById('facilityName').value = data.name;
                document.getElementById('locationName').value = data.location;
                document.getElementById('facilityDescription').value = data.description;
                document.getElementById('openTime').value = data.opening;
                document.getElementById('closeTime').value = data.closing;
                document.getElementById('status').value = data.status;
                document.getElementById('bookingStatus').value = data.booking_status;
                document.getElementById('capacity').value = data.capacity;
                
                document.getElementById('editfacilityModal').classList.remove('hidden');
                // เปลี่ยน action ของฟอร์มให้ส่งข้อมูลไปยัง URL สำหรับการแก้ไข
                document.getElementById('editfacilityForm').action = `/booking/facilities/edit/${facilityId}/`;
            })
            .catch(error => console.error('Error fetching facility data:', error));
    });
});


// View facility
const viewFacility = document.getElementById('viewFacilityBtn')
if(viewFacility){
    document.getElementById('viewFacilityBtn').addEventListener('click', function() {
        document.getElementById('viewfacilityModal').classList.remove('hidden');
    });
}


document.querySelectorAll('.view-btn').forEach(button => {
    button.addEventListener('click', function () {
        const facilityId = this.getAttribute('data-id');
        fetch(`view/${facilityId}/`, {
            method: 'GET',
            headers: {
                'X-CSRFToken': csrfToken,
            },
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('viewfacilityModal').classList.remove('hidden'); // เปิด modal ดูข้อมูล
            // เติมข้อมูลใน modal
            document.getElementById('facilityNameView').innerText = data.name;
            document.getElementById('locationNameView').innerText = data.location;
            document.getElementById('facilityDescriptionView').innerText = data.description;
            document.getElementById('openTimeView').innerText = data.opening;
            document.getElementById('closeTimeView').innerText = data.closing;
            document.getElementById('statusView').innerText = data.status;
            document.getElementById('bookingStatusView').innerText = data.booking_status;
            document.getElementById('capacityView').innerText = data.capacity;
        });
    });
});

// ปิดหน้าต่าง
document.querySelectorAll('.cancel-btn, .editcancel-btn, .close-btn').forEach(button => {
    button.addEventListener('click', function () {
        document.getElementById('facilityModal').classList.add('hidden');
        document.getElementById('editfacilityModal').classList.add('hidden');
        document.getElementById('viewfacilityModal').classList.add('hidden');
    });
});


const addFacilityBtn = document.getElementById('addFacilityBtn');
if (addFacilityBtn) {
    addFacilityBtn.addEventListener('click', function() {
        document.getElementById('facilityModal').classList.remove('hidden');
    });
}

