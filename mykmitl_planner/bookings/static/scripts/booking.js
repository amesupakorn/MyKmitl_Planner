document.getElementById('statusFilter').addEventListener('change', function() {
    let filter = this.value;
    let table = document.getElementById('bookingTable');
    let rows = table.getElementsByTagName('tr');

    for (let i = 0; i < rows.length; i++) {
        let status = rows[i].getAttribute('data-status');

        if (filter === "" || status === filter) {
            rows[i].style.display = "";
        } else {
            rows[i].style.display = "none";
        }
    }
});



document.getElementById('searchInput').addEventListener('input', function() {
    const filter = this.value.toLowerCase();
    const listItems = document.querySelectorAll('#bookingTable tr');

    listItems.forEach(function(item) {
        if (item.textContent.toLowerCase().includes(filter)) {
            item.style.display = '';
        } else {
            item.style.display = 'none';
        }
    });
});