function deleteEvent(eventId) {
    fetch('', {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            event_id: eventId
        })
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/booking/event-list/';  
        } else {
            alert('Failed to delete event.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}