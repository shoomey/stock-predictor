// scripts.js

document.addEventListener("DOMContentLoaded", function() {
  // Example: Add event listeners for buttons or other interactive elements

  // If you have a button to fetch predictions, you could add an event listener here
  const predictionButtons = document.querySelectorAll('.prediction-button');
  
  predictionButtons.forEach(button => {
      button.addEventListener('click', function(event) {
          const stockName = event.target.dataset.stockName;
          fetch(`/predict`, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({ stock_name: stockName })
          })
          .then(response => response.json())
          .then(data => {
              // Handle the response data (update the UI accordingly)
              console.log(data);
              // You can display predictions in a modal or update a section of the page
          })
          .catch(error => {
              console.error('Error fetching predictions:', error);
          });
      });
  });

  // Add more interactive features as needed
});
