function showDetails(id) {
    fetch(`/api/receipt/${id}`)
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
              <p><strong>Merchant:</strong> ${receipt.address}</p>
              <p><strong>Date:</strong> ${receipt.datetime}</p>
              </br>
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
  