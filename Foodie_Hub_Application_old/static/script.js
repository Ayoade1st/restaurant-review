// Sample data for featured reviews (replace with your actual data)
const featuredReviews = [
  {
    restaurant: "The Italian Place",
    rating: 4.5,
    review: "Amazing food and service! Highly recommend the pasta dishes."
  },
  {
    restaurant: "Sushi Delight",
    rating: 4,
    review: "Fresh and delicious sushi. Great for a casual lunch or dinner."
  }
];

// Function to generate review cards
function generateReviewCards() {
  const reviewContainer = document.querySelector(".featured-reviews .row");
  featuredReviews.forEach(review => {
    const reviewCard = `
      <div class="col-md-4">
        <div class="review-card">
          <h3>${review.restaurant}</h3>
          <p>Rating: ${review.rating}/5</p>
          <p>${review.review}</p>
        </div>
      </div>
    `;
    reviewContainer.innerHTML += reviewCard;
  });
}

// Call the function to generate review cards on page load
generateReviewCards();