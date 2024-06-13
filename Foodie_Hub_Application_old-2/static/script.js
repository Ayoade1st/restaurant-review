// Sample data for featured reviews (replace with your actual data)
const featuredReviews = [
  {
    restaurant: "The Italian Place",
    rating: 4.5,
    review: "Amazing food and service! Highly recommend the pasta dishes.",
    image: "static/images/1.jpeg" // Placeholder image
  },
  {
    restaurant: "Sushi Delight",
    rating: 4,
    review: "Fresh and delicious sushi. Great for a casual lunch or dinner.",
    image: "static/images/2.jpeg" // Placeholder image
  },
  {
    restaurant: "Delight",
    rating: 4,
    review: "Fresh and delicious sushi. Great for a casual lunch or dinner.",
    image: "static/images/3.jpeg" // Placeholder image
  }
];

// Function to generate review cards
function generateReviewCards() {
  const reviewContainer = document.querySelector(".featured-reviews .row");

  if (reviewContainer) {
    featuredReviews.forEach(review => {
      const reviewCard = `
        <div class="col-md-4">
          <div class="review-card">
            <h3>${review.restaurant}</h3>
            <p>Rating: ${review.rating}/5</p>
            <p>${review.review}</p>
            <img src="${review.image}" alt="${review.restaurant} review image">
          </div>
        </div>
      `;
      reviewContainer.innerHTML += reviewCard;
    });
  } else {
    console.error("Error: Could not find the review container element.");
  }
}
// Call the function to generate review cards on page load
generateReviewCards();


document.addEventListener('DOMContentLoaded', (event) => {
  // Initialize all tooltip components
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })

  // Initialize all popover components
  var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-toggle="popover"]'))
  var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
    return new bootstrap.Popover(popoverTriggerEl)
  })

  // Add any other Bootstrap component initializations here
});
