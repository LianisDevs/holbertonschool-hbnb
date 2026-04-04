document.addEventListener('DOMContentLoaded', async () => {
    // get the value of a cookie using it's name
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`); // split the string after name of value/cookie
        if (parts.length === 2) return parts.pop().split(';').shift();
    }

    const authToken = getCookie('token');
    const loginButton = document.getElementById('login-link');
    const logoutButton = document.getElementById('logout-btn');
    const placesContainer = document.getElementById('places-list');
    const createPlaceSection = document.getElementById('create-place-section');
    const createPlaceForm = document.getElementById('create-place-form');
    const createPlaceMsg = document.getElementById('create-place-msg');
    const createPlaceToggleSection = document.getElementById('create-place-toggle-section');
    const createPlaceToggleBtn = document.getElementById('create-place-toggle-btn');

    if (authToken) {
        loginButton.style.display = 'none';
        if (logoutButton) logoutButton.style.display = 'inline-block';

        // show toggle button, keep form hidden initially
        if (createPlaceToggleSection) createPlaceToggleSection.style.display = 'block';
        if (createPlaceSection) createPlaceSection.style.display = 'none';

        console.log('User is signed in');
    } else {
        if (logoutButton) logoutButton.style.display = 'none';
        if (createPlaceToggleSection) createPlaceToggleSection.style.display = 'none';
        if (createPlaceSection) createPlaceSection.style.display = 'none';
        console.log('User is not signed in');
    }

    if (logoutButton) {
        logoutButton.addEventListener("click", () => {
            document.cookie = "token=; Max-Age=0; path=/";
            window.location.reload(); // stay on index.html
        });
    }

    async function fetchPlaces() {

        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': authToken ? `Bearer ${authToken}` : ''
                }
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const places = await response.json();
            placesContainer.innerHTML = '';

            // display the places in place cards
            places.forEach(place => {
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

                placesContainer.appendChild(article);
            })

        } catch (error) {
            console.error('Could not fetch places:', error);
        }
    }
    await fetchPlaces();

    placesContainer.addEventListener("click", (event) => {
      if (event.target.classList.contains("details-button")) {
        const placeId = event.target.getAttribute("data-id");
        window.location.href = `place.html?id=${placeId}`;
      }
    });

    const filterPrice = document.getElementById('price-filter');

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

    async function createPlace(payload) {
        const response = await fetch('/api/v1/places/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${authToken}`
            },
            body: JSON.stringify(payload)
        });

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
        return response.json();
    }

    if (createPlaceForm) {
        createPlaceForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            if (!authToken) return;

            const titleEl = document.getElementById('place-title');
            const descEl = document.getElementById('place-description');
            const priceEl = document.getElementById('place-price');
            const latEl = document.getElementById('place-latitude');
            const lonEl = document.getElementById('place-longitude');

            const price = Number(priceEl?.value);
            const latitude = Number(latEl?.value);
            const longitude = Number(lonEl?.value);

            if (!titleEl?.value?.trim() || !Number.isFinite(price) || !Number.isFinite(latitude) || !Number.isFinite(longitude)) {
                if (createPlaceMsg) createPlaceMsg.textContent = 'Please fill all required fields with valid numbers.';
                return;
            }

            const payload = {
                title: titleEl.value.trim(),
                description: descEl?.value?.trim() || '',
                price,
                latitude,
                longitude
            };

            try {
                await createPlace(payload);
                if (createPlaceMsg) createPlaceMsg.textContent = 'Place created.';
                createPlaceForm.reset();
                await fetchPlaces(); // refresh existing listings
            } catch (error) {
                if (createPlaceMsg) createPlaceMsg.textContent = error.message;
                console.error(error);
            }
        });
    }

    if (createPlaceToggleBtn) {
        createPlaceToggleBtn.addEventListener('click', () => {
            const isHidden = createPlaceSection.style.display === 'none' || createPlaceSection.style.display === '';
            createPlaceSection.style.display = isHidden ? 'block' : 'none';
            createPlaceToggleBtn.textContent = isHidden ? 'Hide Create Place' : 'Create Place';
        });
    }
});