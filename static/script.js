// Handle opening and closing the popup
var popup = document.getElementById("bookFormPopup");
var btn = document.getElementById("addBookButton");
var closeBtn = document.getElementById("closeButton");

// When the "Add Book" button is clicked, open the modal
btn.onclick = function() {
    popup.style.display = "block";
}

// When the close button (x) is clicked, close the modal
closeBtn.onclick = function() {
    popup.style.display = "none";
}

// When the user clicks anywhere outside the popup, close the modal
window.onclick = function(event) {
    if (event.target == popup) {
        popup.style.display = "none";
    }
}

// Handle the form submission using JavaScript (to send data via fetch)
document.getElementById('addBookForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent default form submission

    // Gather the form data
    const bookData = {
        title: document.getElementById('title').value,
        // author: document.getElementById('author').value,
        rating: document.getElementById('rating').value,
        status: document.getElementById('status').value,
        progress: document.getElementById('progress').value,
        total_pages: document.getElementById('total_pages').value
    };

    // Send the form data to the Flask backend via a POST request
    fetch('/add_book', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(bookData)
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Show a success message (or error)
        popup.style.display = 'none'; // Close the popup after successful submission
    })
    .catch(error => {
        console.error('Error:', error);
    });
});