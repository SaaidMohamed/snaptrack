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
          <p><strong>Address:</strong> ${receipt.address}</p>
          <p><strong>Date & Time:</strong> ${receipt.datetime}</p>
          <p><strong>Total:</strong> ${receipt.total}</p>
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
            </tbody>
          </table>
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
  