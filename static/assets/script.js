// function uploadImage() {
//     var fileInput = document.getElementById('imageUpload');
//     var formData = new FormData();
//     formData.append('file', fileInput.files[0]);

//     // Show original image before uploading
//     var reader = new FileReader();
//     reader.onload = function (e) {
//         document.getElementById('originalImage').src = e.target.result;
//         document.getElementById('originalImage').style.display = 'block';
//     }
//     reader.readAsDataURL(fileInput.files[0]);

//     // Upload the image asynchronously via Fetch API
//     fetch('http://127.0.0.1:5000/upload', {
//         method: 'POST',
//         body: formData,
//     })
//     .then(response => response.json())
//     .then(data => {
//         if (data.edge_image) {
//             // Show the edge-detected image
//             document.getElementById('edgeImage').src = data.edge_image;
//             document.getElementById('edgeImage').style.display = 'block';
//         } else {
//             alert('Error processing image');
//         }
//     })
//     .catch(error => {
//         console.error('Error:', error);
//         alert('There was an error with the image upload');
//     });
// }


document.addEventListener('DOMContentLoaded', function () {
    const uploadButton = document.getElementById('uploadButton');
    const imageInput = document.getElementById('imageUpload');
    const edgeImage = document.getElementById('edgeImage');
    const originalImage = document.getElementById('originalImage');

    uploadButton.addEventListener('click', function () {
        const file = imageInput.files[0];
        
        // Check if a file is selected
        if (!file) {
            alert("Please select an image to upload.");
            return;
        }

        // Show the original image as a preview
        const reader = new FileReader();
        reader.onload = function (e) {
            originalImage.src = e.target.result;
            originalImage.style.display = 'block';
        };
        reader.readAsDataURL(file);

        // Now send the request to Flask
        const formData = new FormData();
        formData.append('file', file);

        console.log("Sending request to Flask server...");
        
        // Send POST request to Flask server
        fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Response received from Flask server.");
            if (data.edge_image) {
                console.log("Edge detection successful. Displaying image.");
                edgeImage.src = data.edge_image;
                edgeImage.style.display = 'block';
            } else {
                console.error("Error processing image.");
                alert('Error processing image');
            }
        })
        .catch(error => {
            console.error('Error in fetch request:', error);  // Detailed error log
            alert('There was an error with the image upload');
        });
    });
});


