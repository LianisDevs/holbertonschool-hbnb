document.addEventListener("DOMContentLoaded", async () => {
  if (!window.location.pathname.endsWith("place.html")) return; // check pathname

  const params = new URLSearchParams(window.location.search); // get place Id
  const placeId = params.get("id");

  // Get token from cookies
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return null;
  }

  const authToken = getCookie("token");
  const loginButton = document.getElementById("login-link");

  //   hide login button
  if (authToken) {
    loginButton.style.display = "none";
  } else {
    loginButton.style.display = "block";
  }
  // check if place id exists in url
  if (!placeId) {
    window.location.href = "index.html";
    return;
  }

  async function fetchPlaceDetails(placeId) {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/v1/places/${placeId}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: authToken ? `Bearer ${authToken}` : "",
          },
        },
      );

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const place = await response.json();
      console.log("place", place);
      return place;
    } catch (error) {
      console.error("Could not fetch place details:", error);
    }
  }

  const place = await fetchPlaceDetails(placeId);

  function displayPlaceDetails(place) {
    const placeDetails = document.getElementById("place-details");

    if (!place) {
      placeDetails.innerHTML = "<p>Place not found.</p>";
      return;
    }

    // Populate place details
    document.getElementById("place-details-title").textContent = place.title;

    document.querySelector(".place-details-image img").src =
      `https://loremflickr.com/800/400/house,mansion,architecture?lock=${place.id}`;
    document.querySelector(".place-details-image img").alt = place.title;

    document.getElementById("place-details-host-info").textContent =
      `${place.owner.first_name} ${place.owner.last_name}`;

    document.getElementById("place-details-price").textContent =
      `$${parseFloat(place.price).toFixed(0)} per night`;

    document.getElementById("place-details-description").textContent =
      place.description;

    // Populate amenities
    const amenitiesList = document.getElementById(
      "place-details-amenities-list",
    );
    amenitiesList.innerHTML =
      place.amenities.length > 0
        ? place.amenities.map((amenity) => `<li>${amenity.name}</li>`).join("")
        : "<li>No amenities listed</li>";

    // Populate reviews
    const reviewsList = document.getElementById("place-details-reviews-list");
    const noReviews = document.getElementById("place-details-no-reviews");

    if (place.reviews && place.reviews.length > 0) {
      noReviews.style.display = "none";
      reviewsList.innerHTML = place.reviews
        .map(
          (review) => `
            <div class="review-card">
                <div class="review-header">
                    <div class="review-author">${review.id}</div>
                    <div class="review-rating">${"★".repeat(review.rating)}${"☆".repeat(5 - review.rating)}</div>
                </div>
                <div class="review-text">${review.text}</div>
            </div>
        `,
        )
        .join("");
    } else {
      reviewsList.innerHTML = "";
      noReviews.style.display = "block";
    }
  }

  displayPlaceDetails(place);
});

function toggleReviewForm() {
  const showFormSection = document.getElementById("show-form-section");
  const formContainer = document.getElementById("review-form-container");
  const showFormBtn = document.getElementById("show-review-form-btn");

  if (
    formContainer.style.display === "none" ||
    formContainer.style.display === ""
  ) {
    // Show the form, hide the button
    formContainer.style.display = "block";
    showFormSection.style.display = "none";
    // Scroll to form
    formContainer.scrollIntoView({ behavior: "smooth" });
  } else {
    // Hide the form, show the button
    formContainer.style.display = "none";
    showFormSection.style.display = "block";
    // Clear form when hiding
    const form = document.getElementById("review-form");
    if (form) {
      form.reset();
      const charCount = document.querySelector(".char-count");
      if (charCount) {
        charCount.textContent = "0/1000 characters";
      }
    }
  }
}