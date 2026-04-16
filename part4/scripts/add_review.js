// Run setup logic after the DOM is fully loaded
document.addEventListener("DOMContentLoaded", async () => {
  // Cache main form/UI elements
  const form = document.getElementById("review-form");
  const reviewText = document.getElementById("review-text");
  const rating = document.getElementById("rating");
  const charCount = document.getElementById("char-count");
  const placeInfo = document.getElementById("place-info-small");
  const errorEl = document.getElementById("review-error");

  // Notification  alert function
  // Show a toast notification with success/error styling
  function showToast(msg, type = "error") {
    const toast = document.getElementById("toast");
    const toastMsg = document.getElementById("toast-message");
    const toastIcon = document.getElementById("toast-icon");

    toastIcon.textContent = type === "success" ? "✓" : "✕";
    toastMsg.textContent = msg;
    toast.className = `toast toast--${type}`;
    toast.classList.add("show");

    // Auto-hide toast after a short delay
    setTimeout(() => {
      toast.classList.remove("show");
    }, 3500);
  }

  // Display an error message via toast
  function showError(msg) {
    // errorEl.textContent = msg;
    // errorEl.style.display = "block";
    showToast(msg, "error");
  }

  // Read a cookie value by name
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return null;
  }

  // Decode JWT payload safely; return empty object on failure
  function decodeJwtPayload(token) {
    try {
      const base64 = token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/");
      const json = decodeURIComponent(
        atob(base64)
          .split("")
          .map((c) => `%${`00${c.charCodeAt(0).toString(16)}`.slice(-2)}`)
          .join(""),
      );
      return JSON.parse(json);
    } catch {
      return {};
    }
  }

  // Get token from cookies
  // Duplicate cookie helper used in auth-related section
  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return null;
  }

  // Cache auth-related UI elements and token
  const authToken = getCookie("token");
  const loginButton = document.getElementById("login-link");
  const logoutButton = document.getElementById("logout-btn");

  //   hide login button
  // Toggle login/logout visibility based on auth token
  if (authToken) {
    loginButton.style.display = "none";
    logoutButton.style.display = "inline-block";
  } else {
    loginButton.style.display = "inline-block";
    logoutButton.style.display = "none";
  }

  // Handle logout click by clearing token and reloading page
  if (logoutButton) {
    logoutButton.addEventListener("click", () => {
      document.cookie = "token=; Max-Age=0; path=/";
      window.location.reload(); // stay on place.html
    });
  }

  // Require token; redirect unauthenticated users
  const token = getCookie("token");
  if (!token) {
    window.location.href = "/part4/html/index.html";
    return;
  }

  // Read place ID from query string
  const params = new URLSearchParams(window.location.search);
  const placeId = params.get("id");
  if (!placeId) {
    showError("Missing place id.");
    form.style.display = "none";
    return;
  }

  // load place
  // Fetch selected place details and render basic info
  let place;
  try {
    const res = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`);
    if (!res.ok) throw new Error("Could not load place.");
    place = await res.json();
    placeInfo.innerHTML = `<h3>${place.title}</h3><p>${place.description || ""}</p>`;
  } catch (e) {
    showError(e.message);
    form.style.display = "none";
    return;
  }

  // block owner from reviewing own place (frontend guard)
  // Extract current user ID from token payload
  const payload = decodeJwtPayload(token);
  const me =
    payload.id ||
    payload.user_id ||
    (typeof payload.sub === "object" ? payload.sub?.id : payload.sub);

  // Prevent owner from submitting a review for their own place
  if (me && place.owner_id && String(me) === String(place.owner_id)) {
    showError("You cannot review your own place.");
    form.style.display = "none";
    return;
  }

  // Update live character counter as user types
  reviewText.addEventListener("input", () => {
    charCount.textContent = `${reviewText.value.length}/1000 characters`;
  });

  // Handle review form submission
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    // errorEl.style.display = "none";

    // Build request payload from form values
    const body = {
      text: reviewText.value.trim(),
      rating: Number(rating.value),
      place_id: placeId,
    };

    // Basic client-side validation
    if (!body.text || !body.rating) {
      showError("Please fill in review text and rating.");
      return;
    }

    // Send create-review request to API
    try {
      const res = await fetch("http://127.0.0.1:5000/api/v1/reviews/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(body),
      });

      // Redirect to login if token is invalid/expired
      if (res.status === 401) {
        window.location.href = "/part4/html/login.html";
        return;
      }

      // Show specific forbidden message (e.g., owner review attempt)
      if (res.status === 403) {
        const errorData = await res.json();
        showError(errorData.error || "You cannot review your own place.");
        return;
      }

      // if (!res.ok) {
      //   const t = await res.text();
      //   throw new Error(t || `Create review failed (${res.status})`);
      // }

      // Show validation/server message for bad request
      if (res.status === 400) {
        const errorData = await res.json();
        showError(errorData.error || "Could not submit review.");
        return;
      }

      // Handle other non-success responses
      if (!res.ok) {
        let errorMessage;
        try {
          const errorData = await res.json();
          errorMessage =
            errorData.error || errorData.message || `Failed (${res.status})`;
        } catch {
          errorMessage = `Something went wrong (${res.status})`;
        }
        throw new Error(errorMessage);
      }

      // Show success feedback, reset form, then redirect back to place page
      showToast("Review submitted successfully!", "success");
      form.reset();
      charCount.textContent = "0/1000 characters";
      console.log("place id", placeId);

      // optional delayed redirect
      setTimeout(() => {
        window.location.href = `/part4/html/place.html?id=${placeId}`;
      }, 800);
    } catch (err) {
      // Show fallback error on request failure
      showError(err.message || "Failed to submit review.");
    }
  });
});
