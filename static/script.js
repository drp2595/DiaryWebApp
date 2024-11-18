document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault();  // Prevent the form from submitting the traditional way
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    const data = {
        username: username,
        password: password
    };

    // Send POST request to the Flask backend login API
    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.redirect) {
            // Redirect to the index page if login is successful
            window.location.href = data.redirect;
        } else {
            // Display error message if login fails
            document.getElementById('error-message').textContent = data.error;
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        document.getElementById('error-message').textContent = "An error occurred. Please try again.";
    });
});
