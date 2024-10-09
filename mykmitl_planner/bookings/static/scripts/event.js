function deleteEvent(eventId) {
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
                Swal.fire('Error!', 'Something went wrong.', 'error');

            });
        }
    });
}