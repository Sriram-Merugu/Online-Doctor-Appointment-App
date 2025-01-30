document.addEventListener('DOMContentLoaded', function() {
    const profileForm = document.getElementById('profileForm');
    
    profileForm.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Get form values
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirmPassword').value;
        
        // Validate password match
        if (password !== confirmPassword) {
            alert('Passwords do not match');
            return;
        }
        
        // Here you can handle form submission, such as sending data to the server or updating local storage
        // For demonstration purposes, we'll just log the form data
        console.log('Name:', name);
        console.log('Email:', email);
        console.log('Password:', password);
        
        // Optionally, you can display a success message or redirect the user to another page
        alert('Profile updated successfully');
    });
});
