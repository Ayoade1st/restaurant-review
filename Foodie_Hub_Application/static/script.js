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
    // Create a document fragment to improve performance
    const fragment = document.createDocumentFragment();

    featuredReviews.forEach(review => {
      // Create elements using createElement for better control
      const reviewCard = document.createElement('div');
      reviewCard.classList.add('col-md-4');

      const cardContent = document.createElement('div');
      cardContent.classList.add('review-card');

      const restaurantHeading = document.createElement('h3');
      restaurantHeading.textContent = review.restaurant;

      const ratingParagraph = document.createElement('p');
      ratingParagraph.textContent = `Rating: ${review.rating}/5`;

      const reviewParagraph = document.createElement('p');
      reviewParagraph.textContent = review.review;

      const reviewImage = document.createElement('img');
      reviewImage.src = review.image;
      reviewImage.alt = `${review.restaurant} review image`;

      // Append elements to the card
      cardContent.appendChild(restaurantHeading);
      cardContent.appendChild(ratingParagraph);
      cardContent.appendChild(reviewParagraph);
      cardContent.appendChild(reviewImage);

      reviewCard.appendChild(cardContent);
      fragment.appendChild(reviewCard);
    });

    // Append the fragment to the container
    reviewContainer.appendChild(fragment);
  } else {
    console.error("Error: Could not find the review container element.");
  }
}

// Call the function to generate review cards on page load
generateReviewCards();


const exploreNowButton = document.getElementById("exploreNowButton");
    exploreNowButton.addEventListener('click', function() {
      window.location.href = "{{ url_for('restaurants') }}"; // Use Flask's url_for
    });


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