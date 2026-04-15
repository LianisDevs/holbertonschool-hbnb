document.addEventListener("DOMContentLoaded", async () => {
  const form = document.getElementById("review-form");
  const reviewText = document.getElementById("review-text");
  const rating = document.getElementById("rating");
  const charCount = document.getElementById("char-count");
  const placeInfo = document.getElementById("place-info-small");
  const errorEl = document.getElementById("review-error");
  // Notification  alert function
  function showToast(msg, type = "error") {
    const toast = document.getElementById("toast");
    const toastMsg = document.getElementById("toast-message");
    const toastIcon = document.getElementById("toast-icon");

    toastIcon.textContent = type === "success" ? "✓" : "✕";
    toastMsg.textContent = msg;
    toast.className = `toast toast--${type}`;
    toast.classList.add("show");

    setTimeout(() => {
      toast.classList.remove("show");
    }, 3500);
  }
  function showError(msg) {
    // errorEl.textContent = msg;
    // errorEl.style.display = "block";
    showToast(msg, "error");
  }

  function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return null;
  }

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

  const token = getCookie("token");
  if (!token) {
    window.location.href = "/part4/html/index.html";
    return;
  }

  const params = new URLSearchParams(window.location.search);
  const placeId = params.get("id");
  if (!placeId) {
    showError("Missing place id.");
    form.style.display = "none";
    return;
  }

  // load place
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
  const payload = decodeJwtPayload(token);
  const me =
    payload.id ||
    payload.user_id ||
    (typeof payload.sub === "object" ? payload.sub?.id : payload.sub);

  if (me && place.owner_id && String(me) === String(place.owner_id)) {
    showError("You cannot review your own place.");
    form.style.display = "none";
    return;
  }

  reviewText.addEventListener("input", () => {
    charCount.textContent = `${reviewText.value.length}/1000 characters`;
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    // errorEl.style.display = "none";

    const body = {
      text: reviewText.value.trim(),
      rating: Number(rating.value),
      place_id: placeId,
    };

    if (!body.text || !body.rating) {
      showError("Please fill in review text and rating.");
      return;
    }

    try {
      const res = await fetch("http://127.0.0.1:5000/api/v1/reviews/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(body),
      });

      if (res.status === 401) {
        window.location.href = "/part4/html/login.html";
        return;
      }
      if (res.status === 403) {
        const errorData = await res.json();
        showError(errorData.error || "You cannot review your own place.");
        return;
      }
      // if (!res.ok) {
      //   const t = await res.text();
      //   throw new Error(t || `Create review failed (${res.status})`);
      // }
      if (res.status === 400) {
        const errorData = await res.json();
        showError(errorData.error || "Could not submit review.");
        return;
      }
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
      showToast("Review submitted successfully!", "success");
      form.reset();
      charCount.textContent = "0/1000 characters";
      console.log('place id', placeId)
      // optional delayed redirect
      setTimeout(() => {
          window.location.href = `/part4/html/place.html?id=${placeId}`;
      }, 800);
    } catch (err) {
      showError(err.message || "Failed to submit review.");
    }
  });
});
