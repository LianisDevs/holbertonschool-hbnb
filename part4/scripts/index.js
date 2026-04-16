// Run setup once the page is fully loaded
document.addEventListener('DOMContentLoaded', async () => {
    // get the value of a cookie using it's name
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`); // split the string after name of value/cookie
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    // Cache auth state and key DOM elements
    const authToken = getCookie('token');
    const loginButton = document.getElementById('login-link');
    const logoutButton = document.getElementById('logout-btn');
    const placesContainer = document.getElementById('places-list');
    const createPlaceSection = document.getElementById('create-place-section');
    const createPlaceForm = document.getElementById('create-place-form');
    const createPlaceMsg = document.getElementById('create-place-msg');
    const createPlaceToggleSection = document.getElementById('create-place-toggle-section');
    const createPlaceToggleBtn = document.getElementById('create-place-toggle-btn');

    // Cache hero slideshow elements
    const heroImg = document.getElementById('hero-slide');
    const slideA = document.getElementById('hero-slide-a');
    const slideB = document.getElementById('hero-slide-b');

    // Single-image hero slideshow
    if (heroImg) {
        const slides = [
            '/part4/images/hero1.jpg',
            '/part4/images/hero2.jpg',
            '/part4/images/hero3.jpg'
        ];

        // preload slides to avoid flicker
        slides.forEach((src) => {
            const img = new Image();
            img.src = src;
        });

        let i = 0;
        const FADE_MS = 900;
        const INTERVAL_MS = 5500;

        // Rotate hero images with fade effect
        setInterval(() => {
            i = (i + 1) % slides.length;

            heroImg.style.opacity = '0';

            setTimeout(() => {
                heroImg.src = slides[i];
                requestAnimationFrame(() => {
                    heroImg.style.opacity = '1';
                });
            }, FADE_MS);
        }, INTERVAL_MS);
    }

    // Two-layer crossfade hero slideshow
    if (slideA && slideB) {
        const slides = [
            '/part4/images/hero1.jpg',
            '/part4/images/hero2.jpg',
            '/part4/images/hero3.jpg',
            '/part4/images/hero4.jpg',
            '/part4/images/hero5.jpg',
            '/part4/images/hero6.jpg',
            '/part4/images/hero7.jpg',
            '/part4/images/hero8.jpg',
            '/part4/images/hero9.jpg'
        ];

        // preload
        slides.forEach((src) => {
            const img = new Image();
            img.src = src;
        });

        let idx = 0;
        let active = slideA;
        let inactive = slideB;

        // ensure initial state
        active.src = slides[idx];
        active.classList.add('is-active');
        inactive.classList.remove('is-active');

        // Swap active/inactive layers for smooth crossfade
        setInterval(() => {
            idx = (idx + 1) % slides.length;

            // prepare next image under current one
            inactive.src = slides[idx];

            // next frame: crossfade (no blank gap)
            requestAnimationFrame(() => {
                inactive.classList.add('is-active');
                active.classList.remove('is-active');

                // swap refs
                const tmp = active;
                active = inactive;
                inactive = tmp;
            });
        }, 5000);
    }

    // Show/hide auth-related UI based on token presence
    if (authToken) {
        loginButton.style.display = 'none';
        if (logoutButton) logoutButton.style.display = 'inline-block';

        // show toggle button, keep form hidden initially
        if (createPlaceToggleSection) createPlaceToggleSection.style.display = 'block';
        if (createPlaceSection) createPlaceSection.classList.remove("is-open"); // start closed

        console.log('User is signed in');
    } else {
        if (logoutButton) logoutButton.style.display = 'none';
        if (createPlaceToggleSection) createPlaceToggleSection.style.display = 'none';
        if (createPlaceSection) createPlaceSection.classList.remove("is-open");
        console.log('User is not signed in');
    }

    // Clear token and refresh page on logout
    if (logoutButton) {
        logoutButton.addEventListener("click", () => {
            document.cookie = "token=; Max-Age=0; path=/";
            window.location.reload(); // stay on index.html
        });
    }
// function to fetch places for index
    async function fetchPlaces() {

        try {
            // Request place list from API
            const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': authToken ? `Bearer ${authToken}` : ''
                }
            });

            // Stop if request failed
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const places = await response.json();
            // Reset list before rendering
            placesContainer.innerHTML = '';

            // display the places in place cards
            places.forEach(place => {
                // Build a card for each place
                const article = document.createElement('article');
                article.className = 'place-card';

                console.log(place)

                article.innerHTML = `
                        <div class="place-image">
                        <span class="place-image-span">
                         <img class="place-image" src="https://loremflickr.com/400/300/house,mansion,architecture?lock=${place.id}">
                        </span>
                        </div>
                         <div class="place-title">
                         <p>${place.title}</p>
                         <div class="place-price">$${parseFloat(place.price).toFixed(0)}</div>
                         </div>
                         <p class="place-description">${place.description}</p>

                         <button class="details-button" data-id="${place.id}">View Details</button>
                         `;

                // Add card to DOM
                placesContainer.appendChild(article);
            })

        } catch (error) {
            // Log API or render errors
            console.error('Could not fetch places:', error);
        }
    }
    // Initial fetch on page load
    await fetchPlaces();

    // Navigate to place details when clicking a card button
    placesContainer.addEventListener("click", (event) => {
      if (event.target.classList.contains("details-button")) {
        const placeId = event.target.getAttribute("data-id");
        window.location.href = `place.html?id=${placeId}`;
      }
    });

    // Cache price filter element
    const filterPrice = document.getElementById('price-filter');
// filter prices function
    // Filter visible cards by selected max price
    filterPrice.addEventListener('change', (event) => {
        const selectedPrice = event.target.value;
        const placeCards = placesContainer.querySelectorAll('.place-card');

        placeCards.forEach(card => {
            const priceText = card.querySelector('.place-price').textContent;

            const placePrice = parseFloat(priceText.replace('$', ''));

            if (selectedPrice === 'all' || placePrice <= parseFloat(selectedPrice)) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        })
    })
// function for creating a place if authenticated user
    async function createPlace(payload) {
        // Send create-place request
        const response = await fetch('/api/v1/places/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(payload)
        });
// error messaging for creating place
        if (!response.ok) {
            let details = '';
            try {
                const errJson = await response.json();
                details = errJson.message || JSON.stringify(errJson);
            } catch {
                details = await response.text();
            }
            throw new Error(`Create failed: ${response.status} ${details}`);
        }
        // Return created place JSON
        return response.json();
    }

    // Handle create-place form submit
    if (createPlaceForm) {
        createPlaceForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            if (!authToken) return;

            // Read form fields
            const titleEl = document.getElementById('place-title');
            const descEl = document.getElementById('place-description');
            const priceEl = document.getElementById('place-price');
            const latEl = document.getElementById('place-latitude');
            const lonEl = document.getElementById('place-longitude');

            // Convert numeric inputs
            const price = Number(priceEl?.value);
            const latitude = Number(latEl?.value);
            const longitude = Number(lonEl?.value);

            // Validate required values
            if (!titleEl?.value?.trim() || !Number.isFinite(price) || !Number.isFinite(latitude) || !Number.isFinite(longitude)) {
                if (createPlaceMsg) createPlaceMsg.textContent = 'Please fill all required fields with valid numbers.';
                return;
            }

            // Build request payload
            const payload = {
                title: titleEl.value.trim(),
                description: descEl?.value?.trim() || '',
                price,
                latitude,
                longitude
            };

            try {
                // Create place and refresh list
                await createPlace(payload);
                if (createPlaceMsg) createPlaceMsg.textContent = 'Place created.';
                createPlaceForm.reset();
                await fetchPlaces(); // refresh existing listings
            } catch (error) {
                // Show submit error
                if (createPlaceMsg) createPlaceMsg.textContent = error.message;
                console.error(error);
            }
        });
    }

    // Toggle create-place panel open/closed
    if (createPlaceToggleBtn && createPlaceSection) {
        createPlaceToggleBtn.addEventListener("click", () => {
            const open = createPlaceSection.classList.toggle("is-open");
            createPlaceToggleBtn.textContent = open ? "Hide Create Place" : "Create Place";
        });
    }

    // Header: expanded only at top, minimized when scrolled
    const header = document.querySelector('header');
    const TOP_THRESHOLD = 8;
    const mainEl = document.querySelector('main');

    // Get scroll position from window or nested scroll containers
    function getScrollTop() {
        const doc = document.documentElement;
        const body = document.body;
        const scrollingEl = document.scrollingElement;

        return Math.max(
            window.scrollY || 0,
            doc ? doc.scrollTop : 0,
            body ? body.scrollTop : 0,
            scrollingEl ? scrollingEl.scrollTop : 0,
            mainEl ? mainEl.scrollTop : 0
        );
    }

    // Apply header class based on current scroll position
    function syncHeaderState() {
        if (!header) return;
        const y = getScrollTop();
        header.classList.toggle('is-expanded', y <= TOP_THRESHOLD);
    }

    // Set initial header state
    syncHeaderState();

    // catch scroll from window OR nested scroll containers
    window.addEventListener('scroll', syncHeaderState, { passive: true });
    document.addEventListener('scroll', syncHeaderState, { passive: true, capture: true });
    if (mainEl) mainEl.addEventListener('scroll', syncHeaderState, { passive: true });
    window.addEventListener('resize', syncHeaderState, { passive: true });
});