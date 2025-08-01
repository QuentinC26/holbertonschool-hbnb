/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            let email = document.getElementById("email").value;
            let password = document.getElementById("password").value;
            console.log(email, password)
            loginUser(email, password);
        });
    }
    checkAuthentication();
  });

async function loginUser(email, password) {
    const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({email, password})
    })
    if (response.ok) {
      const data = await response.json();
      document.cookie = `token=${data.access_token}; path=/`;
      window.location.href = 'index.html';
    } else {
        alert('Login failed: ' + response.statusText);
    }
  }
  
function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');
    const addReviewSection = document.getElementById('add-review');

    if (!token) {
        loginLink.style.display = 'block';
    } else {
        loginLink.style.display = 'none';
        // Fetch places data if the user is authenticated
        fetchPlaces(token);
    }
      const PlaceId = getPlaceIdFromURL();
    if (!token) {
        addReviewSection.style.display = 'none';
    } 
    if (token && PlaceId) {
      addReviewSection.style.display = 'block';
      fetchPlaceDetails(token, PlaceId);
    } else {
      console.warn("No valid PlaceId, skipping fetchPlaceDetails");
    }
}

function getCookie(name) {
    // Function to get a cookie value by its name
    let new_name = name + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let cut = decodedCookie.split(';');
    for (let index = 0; index < cut.length; index++) {
      let value = cut[index];
      while (value.charAt(0) == ' ') {
        value = value.substring(1);
      }
      if (value.indexOf(new_name) == 0) {
        return value.substring(new_name.length, value.length);
      }
    }
    return "";
  }

async function fetchPlaces(token) {
    // Make a GET request to fetch places data
    // Include the token in the Authorization header
    // Handle the response and pass the data to displayPlaces function
    const response = await fetch('http://127.0.0.1:5000/api/v1/places/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            "Authorization": "Bearer" + " " + token
        },
    })
    if (response.ok) {
      const data_places = await response.json();
      displayPlaces(data_places)
    } else {
        alert('The place are not here' + response.statusText);
    }
}

function displayPlaces(places) {
    // Clear the current content of the places list
    // Iterate over the places data
    // For each place, create a div element and set its content
    // Append the created element to the places list
    document.getElementById('places-list').innerHTML = '';
    const placesList = document.getElementById('places-list');
    if (!placesList) {
      return;
    }   
    for (index2 in places) {
      const place = places[index2];
      let div = document.createElement("div");
      let title = document.createElement("h2");
      let space_one = document.createElement("br");
      let price = document.createElement("p");
      let space_two = document.createElement("br");
      let view_details_link = document.createElement("a");
      let details_img = document.createElement("img");

      title.innerText = places[index2].title;
      price.innerText = `$${places[index2].price}`;

      view_details_link.href = `place.html?id=${place.id}`;
      view_details_link.classList.add("details-button");

      details_img.src = "view_details.png";
      details_img.alt = "View details";
      view_details_link.appendChild(details_img);

      div.append(title);
      div.append(space_one);
      div.append(price);
      div.append(space_two);
      div.append(view_details_link);
      
      placesList.append(div)
      div.setAttribute("data-title", place.title);
      div.setAttribute("data-price", place.price);
    }
}

    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
      priceFilter.addEventListener('change', (event) => {
    // Get the selected price value
    // Iterate over the places and show/hide them based on the selected price
    const selectedPrice = event.target.value;
    const the_list = document.querySelectorAll("#places-list div");
    the_list.forEach(filter => {
        const price = filter.getAttribute("data-price");
        if (selectedPrice === 'All' || parseInt(price) <= parseInt(selectedPrice)) {
            filter.style.display = '';
        } else {
            filter.style.display = 'none';
        }
    });
});
}

function getPlaceIdFromURL() {
    // Extract the place ID from window.location.search
    const params = new URLSearchParams(window.location.search);
    const PlaceId = params.get('id');
    if (!PlaceId) {
      console.warn("No place id found in URL");
      return null;
    }
      return PlaceId;
    
}

async function fetchPlaceDetails(token, PlaceId) {
    // Make a GET request to fetch place details
    // Include the token in the Authorization header
    // Handle the response and pass the data to displayPlaceDetails function
    if (!PlaceId) {
      console.warn("fetchPlaceDetails called without PlaceId");
      return;
    }
    const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${PlaceId}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            "Authorization": "Bearer" + " " + token
        },
    })
    if (response.ok) {
      const data = await response.json();
      displayPlaceDetails(data)
    } else {
        alert('Access to this place failed: ' + response.statusText);
    }
  }

function displayPlaceDetails(place) {
    // Clear the current content of the place details section
    // Create elements to display the place details (name, description, price, amenities and reviews)
    // Append the created elements to the place details section
    document.getElementById('place-details').innerHTML = '';
    const placesbyid = document.getElementById('place-details');
    let div = document.createElement("div");
    let title = document.createElement("h2");
    let space_one = document.createElement("br");
    let host = document.createElement("p");
    let space_two = document.createElement("br");
    let description = document.createElement("p");
    let space_three = document.createElement("br");
    let price = document.createElement("p");
    let space_four = document.createElement("br");
    let amenities = document.createElement("p");
    let space_five = document.createElement("br");

    title.innerText = place.title;
    host.innerHTML = "<strong>Host :</strong> " + place.owner.first_name + " " + place.owner.last_name;
    description.innerHTML = "<strong>Description :</strong> " + place.description;
    price.innerHTML = "<strong>Price per night :</strong> " + `$${place.price}`;
    const amenitieslist = (place.amenities || []).map(a => a.name).join(', ');
    amenities.innerHTML = "<strong>Amenities :</strong> " + amenitieslist;

    div.append(title);
    div.append(space_one);
    div.append(host);
    div.append(space_two);
    div.append(description);
    div.append(space_three);
    div.append(price);
    div.append(space_four)
    div.append(amenities)
    div.append(space_five)
      
    placesbyid.append(div)
    div.setAttribute("data-title", place.title);
    div.setAttribute("data-owner", place.owner.first_name + " " + place.owner.last_name);
    div.setAttribute("data-description", place.description);
    div.setAttribute("data-price", place.price);
    div.setAttribute("data-amenities", place.amenities);

    const reviewsbyplace = document.getElementById('reviews');
    reviewsbyplace.innerHTML = '';
    try {
      for (const review of place.reviews) {
        let review_div = document.createElement("div");
        let review_space_one = document.createElement("br");
        let review_all_reviews = document.createElement("h4");
        let review_space_two = document.createElement("br");
        let review_host = document.createElement("p");
        let review_space_three = document.createElement("br");
        let review_description = document.createElement("p");
        let review_space_four = document.createElement("br");
        let review_rating = document.createElement("p");
        let review_space_five = document.createElement("br");

        review_all_reviews.innerText = "All Reviews for this place :"
        review_host.innerHTML = "<strong>Host :</strong> " + review.user.first_name + " " + review.user.last_name;
        review_description.innerHTML = "<strong>Description :</strong> " + review.text;
        review_rating.innerHTML = "<strong>Rating :</strong> " + review.rating;

        review_div.append(review_space_one);
        review_div.append(review_all_reviews);
        review_div.append(review_space_two);
        review_div.append(review_host);
        review_div.append(review_space_three);
        review_div.append(review_description);
        review_div.append(review_space_four);
        review_div.append(review_rating);
        review_div.append(review_space_five);

        reviewsbyplace.append(review_div)
        review_div.setAttribute("data-title", review.review_all_reviews)
        review_div.setAttribute("data-host", review.user.first_name + " " + review.user.last_name);
        review_div.setAttribute("data-text", review.text);
        review_div.setAttribute("data-rating", review.rating);
      }
    } catch (error) {
      console.warn("places.review is missing", error);
    }

    const add_reviews_in_place = document.getElementById('add-review');

    let add_reviews_div = document.createElement("div");
    let add_reviews_space = document.createElement("br")
    let add_reviews_text = document.createElement("h3")
    let add_reviews_link = document.createElement("a");
    let add_reviews_img =  document.createElement("img");
 
    add_reviews_text.innerText = "Add Reviews :";
    add_reviews_link.href = "add_review.html";
    add_reviews_link.classList.add("add-reviews");

    add_reviews_img.src = "add_review.png";
    add_reviews_img.alt = "View add reviews file";
    add_reviews_link.appendChild(add_reviews_img);

    add_reviews_div.append(add_reviews_text)
    add_reviews_div.append(add_reviews_space)
    add_reviews_div.append(add_reviews_link);
    add_reviews_in_place.append(add_reviews_div)
}