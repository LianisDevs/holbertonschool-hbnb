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
  const logoutButton = document.getElementById("logout-btn");

  //   hide login button
  if (authToken) {
    loginButton.style.display = "none";
    logoutButton.style.display = "inline-block";
  } else {
    loginButton.style.display = "inline-block";
    logoutButton.style.display = "none";
  }

  if (logoutButton) {
    logoutButton.addEventListener("click", () => {
      document.cookie = "token=; Max-Age=0; path=/";
      window.location.reload(); // stay on place.html
    });
  }

  const addReviewButton = document.getElementById("add-review-button");
  const showReviewFormBtn = document.getElementById("show-review-form-btn");

  const goToAddReview = () => {
    if (!placeId) return;
    window.location.href = `add_review.html?id=${encodeURIComponent(placeId)}`;
  };

  if (addReviewButton) addReviewButton.addEventListener("click", goToAddReview);
  if (showReviewFormBtn) showReviewFormBtn.addEventListener("click", goToAddReview);

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

  function getReviewerId(review) {
    if (review.user_id) return review.user_id;
    if (typeof review.user === "string") return review.user; // <-- important
    if (review.user && review.user.id) return review.user.id;
    return null;
  }

  function getReviewerNameFromReview(review) {
    if (review.user_name) return review.user_name;
    if (review.user && typeof review.user === "object") {
      const full = review.user.full_name ||
        `${review.user.first_name || ""} ${review.user.last_name || ""}`.trim();
      if (full) return full;
    }
    return null;
  }

  async function fetchUserFullName(userId, authToken) {
    if (!userId) return null;
    try {
      const headers = {};
      if (authToken) headers.Authorization = `Bearer ${authToken}`;

      const res = await fetch(`/api/v1/users/${userId}`, { headers });
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

      // Preload missing reviewer names
      const nameCache = {};
      const missingUserIds = [
        ...new Set(
          place.reviews
            .map((r) => getReviewerId(r))
            .filter(Boolean),
        ),
      ];

      await Promise.all(
        missingUserIds.map(async (uid) => {
          nameCache[uid] = await fetchUserFullName(uid, authToken);
        }),
      );

      reviewsList.innerHTML = place.reviews.map((review) => {
        const reviewerId = getReviewerId(review);
        const directName = getReviewerNameFromReview(review);
        const fallbackName = reviewerId ? nameCache[reviewerId] : null;
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
      }).join("");
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