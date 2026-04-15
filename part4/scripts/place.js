document.addEventListener("DOMContentLoaded", async () => {
  // Only run this script on place.html
  if (!window.location.pathname.endsWith("place.html")) return;

  // Extract the place ID from the URL query string e.g. ?id=abc123
  const params = new URLSearchParams(window.location.search);
  const placeId = params.get("id");

  // Retrieve a cookie value by name
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return null;
  }

  const authToken = getCookie("token");
  const loginButton = document.getElementById("login-link");
  const logoutButton = document.getElementById("logout-btn");

  // Show logout button if user is authenticated, otherwise show login
  if (authToken) {
    loginButton.style.display = "none";
    logoutButton.style.display = "inline-block";
  } else {
    loginButton.style.display = "inline-block";
    logoutButton.style.display = "none";
  }

  // Clear the auth token cookie and reload the page on logout
  if (logoutButton) {
    logoutButton.addEventListener("click", () => {
      document.cookie = "token=; Max-Age=0; path=/";
      window.location.reload();
    });
  }

  const addReviewButton = document.getElementById("add-review-button");
  const showReviewFormBtn = document.getElementById("show-review-form-btn");

  // Navigate to the add review page, passing the current place ID
  const goToAddReview = () => {
    if (!placeId) return;
    window.location.href = `add_review.html?id=${encodeURIComponent(placeId)}`;
  };

  if (addReviewButton) addReviewButton.addEventListener("click", goToAddReview);
  if (showReviewFormBtn)
    showReviewFormBtn.addEventListener("click", goToAddReview);

  // Redirect to home if no place ID is present in the URL
  if (!placeId) {
    window.location.href = "index.html";
    return;
  }

  // Fetch place details from the API by place ID
  async function fetchPlaceDetails(placeId) {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/api/v1/places/${placeId}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            // Include auth token if available (required for protected routes)
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

  // Extract the reviewer's user ID from a review object
  // Handles multiple API response shapes for the user field
  function getReviewerId(review) {
    if (review.user_id) return review.user_id;
    if (typeof review.user === "string") return review.user;
    if (review.user && review.user.id) return review.user.id;
    return null;
  }

  // Extract the reviewer's display name directly from the review object
  // Returns null if no name is embedded (will fall back to API lookup)
  function getReviewerNameFromReview(review) {
    if (review.user_name) return review.user_name;
    if (review.user && typeof review.user === "object") {
      const full =
        review.user.full_name ||
        `${review.user.first_name || ""} ${review.user.last_name || ""}`.trim();
      if (full) return full;
    }
    return null;
  }

  // Fetch a user's full name from the API using their ID
  // Used as a fallback when the review doesn't include reviewer name
  async function fetchUserFullName(userId, authToken) {
    if (!userId) return null;
    try {
      const headers = {};
      if (authToken) headers.Authorization = `Bearer ${authToken}`;

      const res = await fetch(`http://127.0.0.1:5000/api/v1/users/${userId}`, {
        headers,
      });
      if (!res.ok) return null;

      const user = await res.json();
      return (
        user.full_name ||
        `${user.first_name || ""} ${user.last_name || ""}`.trim() ||
        null
      );
    } catch {
      return null;
    }
  }

  async function displayPlaceDetails(place) {
    const placeDetails = document.getElementById("place-details");

    if (!place) {
      placeDetails.innerHTML = "<p>Place not found.</p>";
      return;
    }

    // Populate basic place info
    document.getElementById("place-details-title").textContent = place.title;

    // Use a seeded placeholder image based on place ID for visual consistency
    document.querySelector(".place-details-image img").src =
      `https://loremflickr.com/800/400/house,mansion,architecture?lock=${place.id}`;
    document.querySelector(".place-details-image img").alt = place.title;

    document.getElementById("place-details-host-info").textContent =
      `${place.owner.first_name} ${place.owner.last_name}`;

    document.getElementById("place-details-price").textContent =
      `$${parseFloat(place.price).toFixed(0)} per night`;

    document.getElementById("place-details-description").textContent =
      place.description;

    // Render amenities list, or show fallback if none exist
    const amenitiesList = document.getElementById(
      "place-details-amenities-list",
    );
    amenitiesList.innerHTML =
      place.amenities.length > 0
        ? place.amenities.map((amenity) => `<li>${amenity.name}</li>`).join("")
        : "<li>No amenities listed</li>";

    const reviewsList = document.getElementById("place-details-reviews-list");
    const noReviews = document.getElementById("place-details-no-reviews");

    if (place.reviews && place.reviews.length > 0) {
      noReviews.style.display = "none";

      // Collect all unique reviewer IDs to batch-fetch missing names
      const nameCache = {};
      const missingUserIds = [
        ...new Set(place.reviews.map((r) => getReviewerId(r)).filter(Boolean)),
      ];

      // Fetch all reviewer names in parallel and store in cache
      await Promise.all(
        missingUserIds.map(async (uid) => {
          nameCache[uid] = await fetchUserFullName(uid, authToken);
        }),
      );

      // Render each review card with author name and star rating
      reviewsList.innerHTML = place.reviews
        .map((review) => {
          const reviewerId = getReviewerId(review);
          const directName = getReviewerNameFromReview(review);
          const fallbackName = reviewerId ? nameCache[reviewerId] : null;
          // Prefer name embedded in review, then cached API lookup, then "Anonymous"
          const authorName = directName || fallbackName || "Anonymous";

          return `
            <div class="review-card">
              <div class="review-header">
                <div class="review-author">${authorName}</div>
                <div class="review-rating">${"★".repeat(review.rating)}${"☆".repeat(5 - review.rating)}</div>
              </div>
              <div class="review-text">${review.text}</div>
            </div>
          `;
        })
        .join("");
    } else {
      // No reviews — clear list and show empty state message
      reviewsList.innerHTML = "";
      noReviews.style.display = "block";
    }
  }

  displayPlaceDetails(place);
});

// Toggle the inline review form visibility on place.html
// Shows the form and hides the trigger button, or resets and hides the form
function toggleReviewForm() {
  const showFormSection = document.getElementById("show-form-section");
  const formContainer = document.getElementById("review-form-container");

  if (
    formContainer.style.display === "none" ||
    formContainer.style.display === ""
  ) {
    // Reveal the form and hide the "Add a Review" button
    formContainer.style.display = "block";
    showFormSection.style.display = "none";
    formContainer.scrollIntoView({ behavior: "smooth" });
  } else {
    // Hide the form, restore the button, and reset form fields
    formContainer.style.display = "none";
    showFormSection.style.display = "block";

    const form = document.getElementById("review-form");
    if (form) {
      form.reset();
      const charCount = document.querySelector(".char-count");
      if (charCount) charCount.textContent = "0/1000 characters";
    }
  }
}
