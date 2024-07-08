document.getElementById('operation').addEventListener('change', function() {
    const ksizeInput = document.getElementById('ksize');
    const thresholdInput = document.getElementById('threshold-value');
    if (this.value === 'gaussian_blur') {
        ksizeInput.classList.remove('hidden');
        ksizeInput.required = true;
        thresholdInput.classList.add('hidden');
        thresholdInput.required = false;
    } else if (this.value === 'apply_threshold') {
        ksizeInput.classList.add('hidden');
        ksizeInput.required = false;
        thresholdInput.classList.remove('hidden');
        thresholdInput.required = true;
    } else {
        ksizeInput.classList.add('hidden');
        ksizeInput.required = false;
        thresholdInput.classList.add('hidden');
        thresholdInput.required = false;
    }
});

document.getElementById('image-upload').addEventListener('change', function(event) {
    const [file] = this.files;
    if (file) {
        const uploadedImage = document.getElementById('uploaded-image');
        const uploadedImageContainer = uploadedImage.parentElement;
        const uploadedImageHeading = uploadedImageContainer.previousElementSibling;

        uploadedImage.src = URL.createObjectURL(file);
        uploadedImage.onload = function() {
            URL.revokeObjectURL(uploadedImage.src); // free memory
        }
        uploadedImage.classList.remove('hidden');
        uploadedImageContainer.classList.remove('hidden');
        uploadedImageHeading.classList.remove('hidden');
    }
});

document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch('/process', {
        method: 'POST',
        body: formData
    }).then(response => response.blob())
      .then(blob => {
          const img = document.getElementById('processed-image');
          const processedImageContainer = img.parentElement;
          const processedImageHeading = processedImageContainer.previousElementSibling;

          img.src = URL.createObjectURL(blob);
          img.onload = function() {
              URL.revokeObjectURL(img.src); // free memory
          }
          img.classList.remove('hidden');
          processedImageContainer.classList.remove('hidden');
          processedImageHeading.classList.remove('hidden');
      }).catch(error => {
          console.error('Error:', error);
      });
});

document.getElementById('reset-button').addEventListener('click', function() {
    fetch('/reset', {
        method: 'POST'
    }).then(response => response.blob())
      .then(blob => {
          const img = document.getElementById('processed-image');
          img.src = URL.createObjectURL(blob);
          img.onload = function() {
              URL.revokeObjectURL(img.src); // free memory
          }
      }).catch(error => {
          console.error('Error:', error);
      });
});

// Ensure the ksize field is visible by default when the page loads
window.addEventListener('DOMContentLoaded', (event) => {
    const ksizeInput = document.getElementById('ksize');
    ksizeInput.classList.remove('hidden');
    ksizeInput.required = true;
});
