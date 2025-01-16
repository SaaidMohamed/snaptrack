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

    // Collect main form data
    const formData = new FormData(form);
    const jsonData = {};
    formData.forEach((value, key) => {
        jsonData[key] = value;
    });

    // Collect items data from the table
    const items = [];
    const tableBody = document.getElementById('editable-items-table-body');
    const rows = tableBody.querySelectorAll('tr'); // Get all rows in the table body
 
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
            const result = await response.text();
            document.body.innerHTML = result; 
        } else {
            alert('Error saving data!');
            console.log('Error:', response.statusText);
        }
    } catch (error) {
        console.log('Fetch error:', error);
    }
}


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

    const confirmBtn = document.getElementById('confirm-btn');
    const statusMessage = document.getElementById('status');

    // Disable the button to prevent multiple clicks
    confirmBtn.disabled = true;
    statusMessage.textContent = "Processing...";
    statusMessage.style.color = '#28a745';

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
                const mainContainer = document.getElementById('mainContainer');
                uploadMcontainer.style.display = "none";
                
                const video = document.createElement('video');
                video.srcObject = stream;
                video.play();
                video.style.width = '100%';
                mainContainer.append(video);

                const captureButton = document.createElement('button');
                captureButton.textContent = 'Capture Image';
                captureButton.className = 'pictureBtn';
                mainContainer.append(captureButton);

                const cancelButton = document.createElement('button');
                cancelButton.textContent = 'Cancel';
                cancelButton.className = 'cancel-button';
                mainContainer.append(cancelButton);

                cancelButton.onclick = function () {
                    stream.getTracks().forEach(track => track.stop()); // Stop the camera stream
                    video.remove();
                    captureButton.remove();
                    window.location.href = '/';

                };

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
                    cancelButton.remove();
                };
            })
            .catch(function (err) {
              alert("Error accessing camera: " + err);
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
                label: 'Receipts Total',
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

function showDetails(id) {
    fetch(`/api/receipt`, {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ id })
      })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Receipt not found");
        }
        return response.json();
        
      })
      .then((receipt) => {
        const detailsContainer = document.getElementById("details-container");

        // Build receipt details content
        let content = `
              <p><strong>Merchant:</strong> ${receipt.merchant}</p>
              <p><strong>Address:</strong> ${receipt.address}</p>
              <p><strong>Date:</strong> ${receipt.datetime}</p>
              <table>
                <thead>
                  <tr>
                    <th>Item</th>
                    <th>Qty</th>
                    <th>Price</th>
                  </tr>
                </thead>
                <tbody>
        `;
        receipt.items.forEach((item) => {
          content += `
            <tr>
              <td>${item.name}</td>
              <td>${item.qty}</td>
              <td>${item.price}</td>
            </tr>
          `;
        });
        content += `
            <tfoot>
                  <tr class="total">
                    <td colspan="2">Total</td>
                    <td>${receipt.total}</td>
                  </tr>
                </tfoot>
              </table>
            </div>
          </div>
          <button class="close-button" onclick="closeDetails()">Close</button>
        `;
  
        detailsContainer.innerHTML = content;
        document.getElementById("receipt-details").classList.remove("hidden");
      })
      .catch((error) => {
        console.error(error);
        alert("Error fetching receipt details.");
      });
  }
  
  function closeDetails() {
    document.getElementById("receipt-details").classList.add("hidden");
  }
  