// --- Utility: get cookie by name ---
function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

// --- Utility: extract place ID from URL ---
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

// --- TASK 1: LOGIN ---

async function loginUser(email, password) {
  try {
    const response = await fetch('http://127.0.0.1:5000/api/v1/authentication_token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    if (!response.ok) throw new Error('Login failed');
    const data = await response.json();
    document.cookie = `token=${data.token}; path=/`;
    window.location.href = 'index.html';
  } catch (err) {
    alert('Login failed: ' + err.message);
  }
}

function setupLogin() {
  const loginForm = document.getElementById('login-form');
  if (!loginForm) return;

  loginForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    const email = loginForm.querySelector('input[name="email"]').value.trim();
    const password = loginForm.querySelector('input[name="password"]').value.trim();
    if (!email || !password) {
      alert('Please fill in both email and password.');
      return;
    }
    await loginUser(email, password);
  });
}

// --- TASK 2: INDEX (List places, price filter) ---

async function fetchPlaces(token) {
  try {
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
      method: 'GET',
      headers
    });
    if (!response.ok) throw new Error('Failed to fetch places');
    const places = await response.json();
    displayPlaces(places);
  } catch (error) {
    console.error('Error fetching places:', error);
  }
}

function displayPlaces(places) {
  const placesList = document.getElementById('places-list');
  if (!placesList) return;

  placesList.innerHTML = ''; // clear list

  places.forEach(place => {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.dataset.price = place.price;

    card.innerHTML = `
      <h3>${place.name}</h3>
      <p>Price per night: €${place.price}</p>
      <a href="place.html?id=${place.id}" class="details-button">View Details</a>
    `;

    placesList.appendChild(card);
  });
}

function setupPriceFilter() {
  const filter = document.getElementById('price-filter');
  if (!filter) return;

  filter.addEventListener('change', () => {
    const selectedValue = filter.value;
    const cards = document.querySelectorAll('.place-card');

    cards.forEach(card => {
      const price = parseFloat(card.dataset.price);
      if (selectedValue === 'All' || price <= parseFloat(selectedValue)) {
        card.style.display = 'block';
      } else {
        card.style.display = 'none';
      }
    });
  });
}

function checkAuthenticationIndex() {
  const token = getCookie('token');
  const loginLink = document.getElementById('login-link');

  if (!token) {
    if (loginLink) loginLink.style.display = 'block';
  } else {
    if (loginLink) loginLink.style.display = 'none';
    fetchPlaces(token);
  }
}

// --- TASK 3: PLACE DETAILS ---

async function fetchPlaceDetails(token, placeId) {
  try {
    const headers = { 'Content-Type': 'application/json' };
    if (token) headers['Authorization'] = `Bearer ${token}`;

    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
      method: 'GET',
      headers
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    const place = await response.json();
    displayPlaceDetails(place);
    return place;
  } catch (error) {
    console.error('Error fetching place details:', error);
    const container = document.getElementById('place-details');
    if (container) container.textContent = 'Error loading place details.';
    return null;
  }
}

function displayPlaceDetails(place) {
  const container = document.getElementById('place-details');
  if (!container) return;

  container.innerHTML = '';

  const title = document.createElement('h2');
  title.textContent = place.name;

  const price = document.createElement('p');
  price.innerHTML = `<strong>Price:</strong> €${place.price}`;

  const description = document.createElement('p');
  description.innerHTML = `<strong>Description:</strong> ${place.description}`;

  const amenitiesTitle = document.createElement('h3');
  amenitiesTitle.textContent = 'Amenities';

  const amenitiesList = document.createElement('ul');
  (place.amenities || []).forEach(am => {
    const li = document.createElement('li');
    li.textContent = am.name;
    amenitiesList.appendChild(li);
  });

  const reviewsTitle = document.createElement('h3');
  reviewsTitle.textContent = 'Reviews';

  const reviewsList = document.createElement('div');
  (place.reviews || []).forEach(r => {
    const card = document.createElement('div');
    card.className = 'review-card';
    card.innerHTML = `<p>"${r.text}"</p><small>by ${r.user_name || r.user}: ${r.rating || 'N/A'} ⭐️</small>`;
    reviewsList.appendChild(card);
  });

  container.append(
    title,
    price,
    description,
    amenitiesTitle,
    amenitiesList,
    reviewsTitle,
    reviewsList
  );
}

function checkAuthenticationPlaceDetails() {
  const token = getCookie('token');
  const placeId = getPlaceIdFromURL();
  const addReviewSection = document.getElementById('add-review');

  if (!placeId) {
    alert('No place ID found in URL');
    return;
  }

  if (addReviewSection) {
    addReviewSection.style.display = token ? 'block' : 'none';
  }

  fetchPlaceDetails(token, placeId);
}

// --- TASK 4: ADD REVIEW FORM ---

async function submitReview(token, placeId, reviewText, rating) {
  try {
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ text: reviewText, rating: Number(rating) })
    });

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

    alert('Review submitted successfully!');
    document.getElementById('review-form').reset();

    // Reload place details to show the new review
    const placeDetailsToken = getCookie('token');
    const placeDetailsId = getPlaceIdFromURL();
    fetchPlaceDetails(placeDetailsToken, placeDetailsId);
  } catch (error) {
    alert('Failed to submit review');
    console.error('submitReview error:', error);
  }
}

function setupReviewForm() {
  const reviewForm = document.getElementById('review-form');
  if (!reviewForm) return;

  const token = getCookie('token');
  if (!token) {
    // Not authenticated, redirect to index.html
    window.location.href = 'index.html';
    return;
  }

  const placeId = getPlaceIdFromURL();

  // Display place name on add review page
  fetchPlaceDetails(token, placeId).then(place => {
    if (!place) return;
    const placeNameSpan = document.getElementById('place-name');
    if (placeNameSpan) placeNameSpan.textContent = place.name;
  });

  reviewForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const reviewText = document.getElementById('review').value.trim();
    const rating = document.getElementById('rating').value;
    if (!reviewText) {
      alert('Please write a review before submitting.');
      return;
    }
    await submitReview(token, placeId, reviewText, rating);
  });
}

// --- DOMContentLoaded event: Detect page and init corresponding logic ---

document.addEventListener('DOMContentLoaded', () => {
  if (document.getElementById('login-form')) {
    setupLogin();
  } else if (document.getElementById('places-list')) {
    checkAuthenticationIndex();
    setupPriceFilter();
  } else if (document.getElementById('place-details')) {
    checkAuthenticationPlaceDetails();
    setupReviewForm();
  }
});