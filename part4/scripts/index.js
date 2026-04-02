document.addEventListener('DOMContentLoaded', async () => {
    // get the value of a cookie using it's name
    function getCookie(name) {
        const value = `; ${document.cookie}`;
        const parts = value.split(`; ${name}=`); // split the string after name of value/cookie
        if (parts.length === 2) return parts.pop().split(';').shift();

    }

    const authToken = getCookie('token');
    const loginButton = document.getElementById('login-link')
    const placesContainer = document.getElementById('places-list');

    if (authToken) {
        loginButton.style.display = 'none';
        console.log('User is signed in');
    } else {
        console.log('User is not signed in');
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
});