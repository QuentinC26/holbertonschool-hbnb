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

    if (!token) {
        addReviewSection.style.display = 'none';
    } else {
        addReviewSection.style.display = 'block';
        // Store the token for later use
        fetchPlaceDetails(token, placeId);
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
      if (value.indexOf(name) == 0) {
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

      view_details_link.href = "place.html";
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
      div.setAttribute("data-title", places[index2].title);
      div.setAttribute("data-price", places[index2].price);
      placesList.appendChild(div);
    }
}

document.getElementById('price-filter').addEventListener('change', (event) => {
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

function getPlaceIdFromURL() {
    // Extract the place ID from window.location.search
    PlaceId = window.location.search(place_id)
}

async function fetchPlaceDetails(token, PlaceId) {
    // Make a GET request to fetch place details
    // Include the token in the Authorization header
    // Handle the response and pass the data to displayPlaceDetails function
    const response = await fetch('http://127.0.0.1:5000/api/v1/get/' + PlaceId, {
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
    document.getElementById(placeId).innerHTML = '';
    const placesbyid = document.getElementById(placeId);
    for (index3 in place) {
      const places = place[index3];
      let div = document.createElement("div");
      let title = document.createElement("h2");
      let space_one = document.createElement("br");
      let description = document.createElement("p");
      let space_two = document.createElement("br");
      let price = document.createElement("p");
      let space_three = document.createElement("br");
      let amenities = document.createElement("p");
      let space_four = document.createElement("br");
      let reviews = document.createElement("p")
      let space_five = document.createElement("br");
      let add_reviews_link = document.createElement("a");
      let details_img = document.createElement("img");

      title.innerText = places[index3].title;
      description.innerText = places[index3].description;
      price.innerText = `$${places[index3].price}`;
      amenities.innerText = places[index3].amenities;
      reviews.innerText = places[index3].reviews;

      add_reviews_link.href = "add_reviews.html";
      add_reviews_link.classList.add("details-button");

      details_img.src = "view_details.png";
      details_img.alt = "View details";
      view_details_link.appendChild(details_img);

      div.append(title);
      div.append(space_one);
      div.append(description);
      div.append(space_two);
      div.append(price);
      div.append(space_three)
      div.append(amenities)
      div.append(space_four)
      div.append(reviews)
      div.append(space_five)
      div.append(view_details_link);
      
      placesbyid.append(div)
      div.setAttribute("data-title", places[index3].title);
      div.setAttribute("data-description", places[index3].description);
      div.setAttribute("data-price", places[index3].price);
      div.setAttribute("data-amenities", places[index3].amenities);
      div.setAttribute("data-reviews", places[index3].reviews);
      placesbyid.appendChild(div);
    }
}