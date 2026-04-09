document.addEventListener("DOMContentLoaded", async () => {
  const form = document.getElementById("review-form");
  const reviewText = document.getElementById("review-text");
  const rating = document.getElementById("rating");
  const charCount = document.getElementById("char-count");
  const placeInfo = document.getElementById("place-info-small");
  const errorEl = document.getElementById("review-error");

  function showError(msg) {
    errorEl.textContent = msg;
    errorEl.style.display = "block";
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
          .map((c) => `%${(`00${c.charCodeAt(0).toString(16)}`).slice(-2)}`)
          .join("")
      );
      return JSON.parse(json);
    } catch {
      return {};
    }
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
    const res = await fetch(`/api/v1/places/${placeId}`);
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
    errorEl.style.display = "none";

    const body = {
      text: reviewText.value.trim(),
      rating: Number(rating.value),
      place_id: placeId
    };

    if (!body.text || !body.rating) {
      showError("Please fill in review text and rating.");
      return;
    }

    try {
      const res = await fetch("/api/v1/reviews/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(body)
      });

      if (res.status === 401) {
        window.location.href = "/part4/html/login.html";
        return;
      }
      if (res.status === 403) {
        showError("You cannot review your own place.");
        return;
      }
      if (!res.ok) {
        const t = await res.text();
        throw new Error(t || `Create review failed (${res.status})`);
      }

      // success message + clear form
      errorEl.style.display = "block";
      errorEl.style.color = "#0a7a2f";
      errorEl.textContent = "Review submitted successfully.";
      form.reset();
      charCount.textContent = "0/1000 characters";

      // optional delayed redirect
      setTimeout(() => {
        window.location.href = `/part4/html/place.html?id=${placeId}`;
      }, 800);

    } catch (err) {
      showError(err.message || "Failed to submit review.");
    }
  });
});