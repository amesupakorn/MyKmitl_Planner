function deleteBooking(bookingId) {
    fetch('', {
        method: 'PUT',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            booking_id: bookingId
        })
    })
    .then(response => {
        if (response.ok) {
            window.location.reload(); 
        } else {
            alert('Failed to cancel booking.');
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}