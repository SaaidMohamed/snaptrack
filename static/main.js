const fileInput = document.getElementById('uploadInput');
const previewMContainer = document.getElementById('filePreviewMcontainer');
const uploadMcontainer = document.getElementById('fileUploadMcontainer');
const previewContainer = document.getElementById('filePreviewContainer');
const previewImage = document.getElementById('previewImage');
const fileName = document.getElementById('fileName');
const errorMessage = document.getElementById('errorMessage');
const loadingMessage = document.getElementById('loadingMessage');
const ocrFormBtn = document.getElementById('ocrFormBtn');


async function handleFormSubmission(event) {
    event.preventDefault(); // Prevent the default form submission behavior

    // Get the form element
    const form = document.getElementById('ocrForm');

    // Collect other form data
    const formData = new FormData(form);
    const jsonData = {};
    formData.forEach((value, key) => {
        jsonData[key] = value;
    });

    // Collect items data from the table
    const items = [];
    const tableBody = document.getElementById('editable-items-table-body');
    const rows = tableBody.querySelectorAll('tr'); // Get all rows in the table body
    // Check how many rows are being selected
    console.log('Number of rows found:', rows.length);


    rows.forEach((row) => {
        const cells = row.querySelectorAll('td');
        const item = {
            description: cells[0]?.innerText.trim(),
            amount: parseFloat(cells[1]?.innerText.trim()) || 0,
            qty: parseInt(cells[2]?.innerText.trim(), 10) || 0,
        };
        items.push(item);
    });

    // Add items to the JSON object
    jsonData.items = items;

    // Print the JSON data to verify it's correct
    console.log('JSON Data being sent:', JSON.stringify(jsonData, null, 2));

    // Send JSON data to the backend
    try {
        const response = await fetch('/save-receipt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(jsonData),
        });

        // Handle the response
        if (response.ok) {
            const result = await response.json();
            alert('Data saved successfully!');
            console.log(result);
        } else {
            alert('Error saving data!');
            console.log('Error:', response.statusText);
        }
    } catch (error) {
        console.log('Fetch error:', error);
    }
}

//ocrFormBtn.addEventListener('submit', handleFormSubmission);



function previewFile() {
    previewContainer.style.display = 'none';
    errorMessage.style.display = 'none';
    loadingMessage.style.display = 'none';

    const file = fileInput.files[0];
    if (file) {
        loadingMessage.style.display = 'block';
        const reader = new FileReader();
        
        reader.onload = function (e) {
            loadingMessage.style.display = 'none';
            previewMContainer.style.display = 'block';
            previewContainer.style.display = 'block';
            uploadMcontainer.style.display = 'none';
            previewImage.src = e.target.result;
            fileName.textContent = file.name;
        };

        reader.onerror = function () {
            loadingMessage.style.display = 'none';
            errorMessage.style.display = 'block'; // Show error message if the file can't be read
        };

        if (file.type.startsWith('image/')) {
            reader.readAsDataURL(file);
        } else {
            errorMessage.style.display = 'block';
        }
    }
}


function confirmImage() {
    function base64ToBlob(base64, mime) {
        const byteString = atob(base64.split(',')[1]); // Decode Base64
        const arrayBuffer = new Uint8Array(byteString.length);
      
        for (let i = 0; i < byteString.length; i++) {
          arrayBuffer[i] = byteString.charCodeAt(i);
        }
      
        return new Blob([arrayBuffer], { type: mime });
      }
    
    const base64Data = previewImage.src;
    
    // Extract MIME type (e.g., "image/png")
    const mimeType = base64Data.match(/^data:(.+);base64,/)[1];
    
    // Convert Base64 to Blob
    const blob = base64ToBlob(base64Data, mimeType);
    
    // Create FormData and send to backend
    const formData = new FormData();
    imgName = fileName.textContent.split('.')[0]+'.png'
    console.log(imgName)
    formData.append('image', blob,  imgName);
    
    fetch('/upload', {
    method: 'POST',
    body: formData,
    })
    .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.text(); // Expecting HTML template as text
      })
      .then((html) => {
        document.documentElement.innerHTML = html;
      })
      .catch((error) => console.error('Error:', error));
    
}


function retryUpload() {
    window.location.href = '/';
}


function openCamera() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
                const video = document.createElement('video');
                video.srcObject = stream;
                video.play();
                video.style.width = '100%';
                document.body.appendChild(video);

                const captureButton = document.createElement('button');
                captureButton.textContent = 'Capture Image';
                captureButton.className = 'pictureBtn';
                document.body.appendChild(captureButton);

                captureButton.onclick = function () {

                    const canvas = document.createElement('canvas');
                    canvas.width = video.videoWidth;
                    canvas.height = video.videoHeight;
                    canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height);

                    const imageData = canvas.toDataURL('image/png');
                    previewImage.src = imageData;
                    previewMContainer.style.display = 'block';
                    previewContainer.style.display = 'block';
                    uploadMcontainer.style.display = 'none';
                    
                    stream.getTracks().forEach(track => track.stop()); // Stop the camera stream
                    video.remove();
                    captureButton.remove();
                };
            })
            .catch(function (err) {
                console.log("Error accessing camera: " + err);
            });
    } else {
        alert("Camera not supported on your device.");
    }
}

function createGraph(data) {
    const ctx = document.getElementById('myChart').getContext('2d');
    const labels = data.map(item => item.label); // X-axis labels
    const values = data.map(item => item.value); // Y-axis values

    new Chart(ctx, {
        type: 'bar', // Graph type: bar, line, etc.
        data: {
            labels: labels,
            datasets: [{
                label: 'Analysis Data',
                data: values,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
            }],
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                },
            },
        },
    });
}


async function fetchData() {
    try {
        const response = await fetch('/data'); // Endpoint to fetch data
        if (!response.ok) throw new Error('Failed to fetch data');
        const data = await response.json();
        createGraph(data); // Pass data to graphing function
    } catch (error) {
        console.log('Error fetching data:', error);
    }
}



//for layout.html
/*
document.addEventListener('DOMContentLoaded', function() {
    // Adapted from https://stackoverflow.com/a/10162353
    const html = '<!DOCTYPE ' +
    document.doctype.name +
    (document.doctype.publicId ? ' PUBLIC "' + document.doctype.publicId + '"' : '') +
    (!document.doctype.publicId && document.doctype.systemId ? ' SYSTEM' : '') +
    (document.doctype.systemId ? ' "' + document.doctype.systemId + '"' : '') +
    '>\n' + document.documentElement.outerHTML;
    document.querySelector('form[action="https://validator.w3.org/check"] > input[name="fragment"]').value = html;
});

*/