document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent default form submission

    // Get the selected audio file
    var audioFile = document.getElementById('audioFile').files[0];
    console.log(audioFile)
    
    // Create a FormData object to send file data
    var formData = new FormData();
    formData.append('audioFile', audioFile);

    // Send the file to Flask backend using AJAX or Fetch API
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        }
        throw new Error('Network response was not ok.');
    })
    .then(data => {
        console.log('File uploaded successfully:', data);
        // Handle response from Flask backend if needed
    })
    .catch(error => {
        console.error('Error uploading file:', error);
        // Handle error if needed
    });
});
