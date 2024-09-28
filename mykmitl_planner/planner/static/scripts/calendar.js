let selectedEvent = null; // To store the event being edited

$(document).ready(function() {
    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay,listWeek'
        },
        editable: true,
        eventLimit: 3, 
        events: events,
        
        
        // Event click (show form and populate data)
        eventClick: function(event) {
            selectedEvent = event;
            $('#event-name').val(event.title);
            $('#start-date').val(moment(event.start).format('YYYY-MM-DD HH:mm'));
            $('#end-date').val(moment(event.end).format('YYYY-MM-DD HH:mm'));
            $('#description').val(event.description);
            $('#location').val(event.location);
            $('#activity').val(event.activity);
            $('#color-value').val(event.color);
            $('#event-id').val(event._id);

            // Show form
            $('#create-event').addClass('open').removeClass('hidden');
            $('#calendar-wrapper').addClass('reduced');
            $('#delete-btn').removeClass('hidden')
        },

        // Day click (show empty form for new event)
        dayClick: function(date) {
            const currentDateTime = moment().format('YYYY-MM-DD HH:mm');            
            selectedEvent = null;
            $('#event-name').val('');
            $('#start-date').val(currentDateTime);
            $('#end-date').val('');
            $('#description').val('');
            $('#location').val('');
            $('#activity').val('');
            $('#color-value').val('');
            $('#event-id').val('');

            // Show form
            $('#create-event').addClass('open').removeClass('hidden');
            $('#calendar-wrapper').addClass('reduced');
            $('#delete-btn').addClass('hidden')

        }
    });

 

    // Save Event (Create or Update)
    $('#add-event').on('submit', function(e) {
        e.preventDefault();
            let eventData = {
                event_id: selectedEvent ? selectedEvent.id : null,               
                title: $('#event-name').val(),  // ใช้ id ที่ Django Forms กำหนด (มักจะเป็น id_field_name)
                start_time: moment($('#start-date').val()).format('YYYY-MM-DD HH:mm'),
                end_time: moment($('#end-date').val()).format('YYYY-MM-DD HH:mm'),
                description: $('#description').val(),
                location: $('#location').val(),
                activity: $('#activity').val(),
                color: $('#color-value').val(), 
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            };

            let url = $('#add-event').attr('action');

            // ส่งข้อมูลไปยัง server ผ่าน Fetch API
            fetch(url, {
                method: 'POST',  // ใช้ POST method
                headers: {
                    'Content-Type': 'application/json',  // ส่งข้อมูลเป็น JSON
                    'X-CSRFToken': eventData.csrfmiddlewaretoken  // ส่ง CSRF token เพื่อป้องกัน CSRF attacks
                },
                body: JSON.stringify(eventData)  // แปลงข้อมูลเป็น JSON
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // หากมี event-id แสดงว่ากำลัง update event
                if ($('#event-id').val()) {
                    selectedEvent.title = eventData.title;
                    selectedEvent.start = eventData.start_time;
                    selectedEvent.end = eventData.end_time ? eventData.en_time : null;
                    selectedEvent.description = eventData.description;
                    selectedEvent.location = eventData.location;
                    selectedEvent.activity = eventData.activity;
                    selectedEvent.color = eventData.color;
                    $('#calendar').fullCalendar('updateEvent', selectedEvent);
                } else {
                    // สร้าง event ใหม่ใน FullCalendar
                    $('#calendar').fullCalendar('renderEvent', eventData, true);
    
                }          
                // Reset form และซ่อนฟอร์มหลังจากบันทึก
                $('#add-event')[0].reset();
                $('#create-event').removeClass('open').addClass('hidden');
                $('#calendar-wrapper').removeClass('reduced');
            
                window.location.reload(); 
            })
            .catch(error => {
                console.error('Error:', error);
                alert('There was an error saving the event. Please try again.');
            });
        });
        
      // Delete Event (เพิ่มโค้ดสำหรับการลบที่นี่)
      $('#delete-btn').on('click', function() {
        if (selectedEvent) {
            // ลบกิจกรรมออกจาก FullCalendar
            $('#calendar').fullCalendar('removeEvents', selectedEvent.id);  // ใช้ selectedEvent.id ในการลบ
            $('#create-event').removeClass('open').addClass('hidden');
            $('#calendar-wrapper').removeClass('reduced');

            // หากต้องการลบกิจกรรมจากฐานข้อมูลด้วย
            let deleteUrl = 'delete/' + selectedEvent.id + '/';  // URL สำหรับลบ event
            
            fetch(deleteUrl, {
                method: 'DELETE',
                headers: {
                    'X-CSRFToken': $('input[name="csrfmiddlewaretoken"]').val()
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
            
            })
            .catch(error => {
                console.error('Error:', error);
                alert('There was an error deleting the event. Please try again.');
            });
        }
    });
});






document.addEventListener('DOMContentLoaded', function() {
    setTimeout(function() {
        const messageBox = document.getElementById('message-box');
        if (messageBox) {
            messageBox.style.opacity = '0';
            setTimeout(() => { messageBox.style.display = 'none'; }, 1000); // Hide after fade out
        }
    }, 3000); // 5 วินาที
});

$(document).ready(function() {
    // Close form when clicking the close button
    $('#close-form-btn').on('click', function() {
        $('#create-event').addClass('hidden');  // Hide the form
        $('#calendar-wrapper').removeClass('reduced');  // Expand the calendar
        $('#add-event')[0].reset();  // Reset the form fields
    });
});
