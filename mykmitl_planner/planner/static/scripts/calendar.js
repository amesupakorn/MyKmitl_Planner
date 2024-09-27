let selectedEvent = null; // To store the event being edited


$(document).ready(function() {
    $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        editable: true,
        eventLimit: 3, // Limit events per day

        // Event click (show form and populate data)
        eventClick: function(event) {
            selectedEvent = event;
            $('#event-name').val(event.title);
            $('#start-date').val(moment(event.start).format('YYYY-MM-DD HH:mm'));
            $('#end-date').val(event.end ? moment(event.end).format('YYYY-MM-DD HH:mm') : '');
            $('#color-value').val(event.color);
            $('#event-id').val(event._id);

            // Show form
            $('#create-event').addClass('open').removeClass('hidden');
            $('#calendar-wrapper').addClass('reduced');
        },

        // Day click (show empty form for new event)
        dayClick: function(date) {
            selectedEvent = null;
            $('#event-name').val('');
            $('#start-date').val(date.format('YYYY-MM-DD HH:mm'));
            $('#end-date').val('');
            $('#color-value').val('');
            $('#event-id').val('');

            // Show form
            $('#create-event').addClass('open').removeClass('hidden');
            $('#calendar-wrapper').addClass('reduced');
        }
    });

    // Setup Flatpickr for Start Date and End Date
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

        // Hide form after saving
        $('#add-event')[0].reset();
        $('#create-event').removeClass('open').addClass('hidden');
        $('#calendar-wrapper').removeClass('reduced');
    });

    // Delete Event
    $('#delete-btn').on('click', function() {
        if (selectedEvent) {
            $('#calendar').fullCalendar('removeEvents', selectedEvent._id);
            $('#create-event').removeClass('open').addClass('hidden');
            $('#calendar-wrapper').removeClass('reduced');
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
