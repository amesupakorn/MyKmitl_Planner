let selectedEvent = null; // To store the event being edited

$(document).ready(function() {
    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        editable: true,
        eventLimit: 3,  // จำกัดการแสดง event ต่อวัน

        eventClick: function(event) {
            selectedEvent = event; // Store the event clicked
            $('#event-name').val(event.title);
            $('#start-date').val(moment(event.start).format('YYYY-MM-DD HH:mm'));
            $('#end-date').val(event.end ? moment(event.end).format('YYYY-MM-DD HH:mm') : '');
            $('#selected-color').css('background-color', event.color);
            $('#color-value').val(event.color);
            $('#event-id').val(event._id); // Store event ID
            $('#add-event').removeClass('hidden');
            $('#delete-btn').removeClass('hidden'); // Show delete button
        },

        dayClick: function(date) {
            selectedEvent = null; // Clear selected event
            $('#event-name').val('');
            $('#start-date').val(date.format('YYYY-MM-DD HH:mm'));
            $('#end-date').val('');
            $('#selected-color').css('background-color', '');
            $('#color-value').val('');
            $('#event-id').val(''); // Clear event ID
            $('#add-event').removeClass('hidden');
            $('#delete-btn').addClass('hidden'); // Hide delete button for new event
        }
    });

    // Setup Flatpickr for Start Date and End Date with time selection
    flatpickr('#start-date', {
        enableTime: true,
        dateFormat: "Y-m-d H:i"
    });
    flatpickr('#end-date', {
        enableTime: true,
        dateFormat: "Y-m-d H:i"
    });

    // Save Event (Create or Update)
    $('#add-event').on('submit', function(e) {
        e.preventDefault();
        let eventData = {
            title: $('#event-name').val(),
            start: $('#start-date').val(),
            end: $('#end-date').val(),
            color: $('#color-value').val()
        };

        if ($('#event-id').val()) {
            // Update existing event
            selectedEvent.title = eventData.title;
            selectedEvent.start = eventData.start;
            selectedEvent.end = eventData.end ? eventData.end : null;
            selectedEvent.color = eventData.color;
            $('#calendar').fullCalendar('updateEvent', selectedEvent);
        } else {
            // Create new event
            $('#calendar').fullCalendar('renderEvent', eventData, true);
        }

        // Clear form
        $('#add-event')[0].reset();
        $('#add-event').addClass('hidden');
    });

    // Delete Event
    $('#delete-btn').on('click', function() {
        if (selectedEvent) {
            $('#calendar').fullCalendar('removeEvents', selectedEvent._id);
            $('#add-event').addClass('hidden');
        }
    });

    // Toggle dropdown for color selection
    const dropdownBtn = document.querySelector('.dropdown-btn');
    const dropdownOptions = document.querySelector('.dropdown-options');
    dropdownBtn.addEventListener('click', () => {
        dropdownOptions.style.display = dropdownOptions.style.display === 'block' ? 'none' : 'block';
    });

    // Select a color option
    dropdownOptions.querySelectorAll('div').forEach(option => {
        option.addEventListener('click', () => {
            const color = option.getAttribute('data-color');
            const colorName = option.querySelector('span').innerText;

            dropdownBtn.innerText = colorName;
            dropdownBtn.style.backgroundColor = color;
            $('#color-value').val(color); // Update hidden input with the selected color value
            dropdownOptions.style.display = 'none';
        });
    });

    // Close dropdown if clicked outside
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.custom-dropdown')) {
            dropdownOptions.style.display = 'none';
        }
    });
});
