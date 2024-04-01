document.addEventListener("DOMContentLoaded", function() {
    const emailInfo = document.querySelector('.email-info');
    const modal = document.getElementById('userInfoModal');
    const closeBtn = modal.querySelector('.close');
    let cardContainer = null;

    emailInfo.addEventListener('click', function() {
        const userEmail = emailInfo.dataset.email;
        const username = emailInfo.dataset.username;
        const userImage = emailInfo.querySelector('img').src;

        // Remove existing card if it exists
        if (cardContainer) {
            cardContainer.remove();
        }
        
        // Create a new div element to hold the card
        cardContainer = document.createElement('div');
        cardContainer.classList.add('card');

        // Create card body
        const cardBody = document.createElement('div');
        cardBody.classList.add('card-body');

        // Create card title
        const cardTitle = document.createElement('h5');
        cardTitle.classList.add('card-title');
        cardTitle.textContent = 'User Information';

        // Create input field for username
        const usernameInput = document.createElement('input');
        usernameInput.setAttribute('type', 'text');
        usernameInput.classList.add('form-control', 'mb-2');
        usernameInput.value = username;

        // Create input field for email
        const emailInput = document.createElement('input');
        emailInput.setAttribute('type', 'email');
        emailInput.classList.add('form-control', 'mb-2');
        emailInput.value = userEmail;

        // Create input field for image upload
        const imageInput = document.createElement('input');
        imageInput.setAttribute('type', 'file');
        imageInput.setAttribute('accept', 'image/*');
        imageInput.classList.add('form-control-file', 'mb-2');

        // Create preview for user image
        const imagePreview = document.createElement('img');
        imagePreview.src = userImage;
        imagePreview.alt = 'User Image';
        imagePreview.classList.add('img-thumbnail', 'mb-2');

        // Function to handle file selection and update preview
        imageInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            const reader = new FileReader();
            reader.onload = function(event) {
                imagePreview.src = event.target.result;
            };
            reader.readAsDataURL(file);
        });

        // Create button to submit changes
        const submitBtn = document.createElement('button');
        submitBtn.classList.add('btn', 'btn-primary', 'mb-2');
        submitBtn.textContent = 'Save Changes';
        submitBtn.addEventListener('click', function() {
            const newUsername = usernameInput.value;
            const newEmail = emailInput.value;
            const newImage = imagePreview.src;

            // Create FormData object to send file data
            const formData = new FormData();
            formData.append('image', imageInput.files[0]);

            // Send AJAX request to upload image
            const xhr = new XMLHttpRequest();
            xhr.open('POST', '/bies/upload_image/', true); // Use the correct URL
            xhr.onload = function() {
                if (xhr.status === 200) {
                    // Image uploaded successfully, handle response
                    const response = JSON.parse(xhr.responseText);
                    if (response.success) {
                        // Image uploaded successfully, now update user information
                        // Send AJAX request to update user information with newUsername, newEmail, and newImage
                        // Handle success and error cases
                        alert(`Username updated to: ${newUsername}, Email updated to: ${newEmail}, Image uploaded successfully`);
                    } else {
                        // Handle error
                        alert('Error uploading image');
                    }
                } else {
                    // Handle error
                    alert('Error uploading image');
                }
            };
            xhr.send(formData);
        });

        // Create close button
        closeBtn.addEventListener('click', function() {
            modal.style.display = 'none';
        });

        // Append elements to card body
        cardBody.appendChild(closeBtn);
        cardBody.appendChild(cardTitle);
        cardBody.appendChild(imagePreview);
        cardBody.appendChild(imageInput);
        cardBody.appendChild(usernameInput);
        cardBody.appendChild(emailInput);
        cardBody.appendChild(submitBtn);

        // Append card body to card container
        cardContainer.appendChild(cardBody);

        // Append card container to modal
        modal.appendChild(cardContainer);

        // Show modal
        modal.style.display = 'block';
    });

    // Close modal when close button is clicked
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });
});