// ======================================
// FINAL CLEAN & WORKING FRONTEND SCRIPT
// ======================================

const BASE_URL = "https://evstationlocator.onrender.com/api/accounts/";
const STATIONS_API = BASE_URL + "stations/";
const INITIAL_LIMIT = 8;

let ALL_STATIONS = [];

// --------------------------------------
// 1️⃣ COMMON API CALL FUNCTION
// --------------------------------------
function apiCall(endpoint, method = "GET", data = null) {
  return fetch(BASE_URL + endpoint, {
    method,
    headers: { "Content-Type": "application/json" },
    body: data ? JSON.stringify(data) : null
  })
    .then(res => res.json())
    .catch(err => {
      console.error("API Error:", err);
      return { success: false, message: "Server error" };
    });
}

// --------------------------------------
// 2️⃣ LOAD STATIONS (ONLY 8 ON PAGE LOAD)
// --------------------------------------
function loadStations() {
  fetch(STATIONS_API)
    .then(res => res.json())
    .then(data => {
      // keep only available stations
      ALL_STATIONS = (data.stations || []).filter(s => s.is_available);

      // show only first 8 initially
      renderStations(ALL_STATIONS.slice(0, INITIAL_LIMIT));
    })
    .catch(err => console.error("Station load error:", err));
}

// --------------------------------------
// 3️⃣ RENDER STATIONS
// --------------------------------------
function renderStations(stations) {
  const list = document.getElementById("stationList");
  list.innerHTML = "";

  if (!stations.length) {
    list.innerHTML = "<p class='small-text'>No stations found.</p>";
    return;
  }

  stations.forEach(station => {
    const freeSlots = station.slots_total - station.slots_booked;

    const card = document.createElement("div");
    card.className = "card";

    card.innerHTML = `
      <img src="${station.image_url || ''}" alt="${station.name}">
      <div class="card-body">
        <div class="card-title-row">
          <h4>${station.name}</h4>
          <span class="status-dot status-online"></span>
        </div>

        <p class="small-text">${station.area}</p>

        <div class="card-tags">
          <span class="tag-pill">${station.connector}</span>
          <span class="tag-pill">${station.speed}</span>
          <span class="tag-pill">${freeSlots} free slots</span>
          <span class="tag-pill">₹${station.approx_rate}</span>
        </div>

        <div class="card-foot">
          <span class="small-text">${station.open_now ? "Open now" : "Closed"}</span>
          <span class="small-text">Available</span>
        </div>
      </div>
    `;

    list.appendChild(card);
  });
}
function openHelpPage() { window.location.href = "help.html"; }

// --------------------------------------
// 4️⃣ SEARCH + FILTER STATIONS (SHOW ALL)
// --------------------------------------
document.getElementById("locatorBtn").onclick = function () {
  const area = searchArea.value.toLowerCase();
  const connector = connectorFilter.value;
  const speed = speedFilter.value;
  const openNow = openNowFilter.checked;

  const filtered = ALL_STATIONS.filter(station => {
    if (area && !station.area.toLowerCase().includes(area)) return false;
    if (connector !== "any" && station.connector !== connector) return false;
    if (speed !== "any" && station.speed !== speed) return false;
    if (openNow && !station.open_now) return false;
    return true;
  });

  renderStations(filtered);

  locatorResult.textContent =
    `Found ${filtered.length} available station(s). Showing below ↓`;

  document.getElementById("stations")
    .scrollIntoView({ behavior: "smooth", block: "start" });
};

// --------------------------------------
// 5️⃣ BOOKING LOGIC
// --------------------------------------
const bookingForm = document.getElementById("bookingForm");
const bookingStatus = document.getElementById("bookingStatus");
const bookingList = document.getElementById("bookingList");
const paymentBtn = document.getElementById("paymentBtn");

bookingForm.onsubmit = function (e) {
  e.preventDefault();

  const data = {
    user_name: userName.value,
    vehicle: userVehicle.value,
    connector: bookingConnector.value,
    date: bookingDate.value,
    time: bookingTime.value,
    duration: Number(bookingDuration.value),
    approx_amount: 150
  };

  apiCall("bookings/", "POST", data).then(res => {
    if (res.success) {
      bookingStatus.textContent = "Booking created!";
      bookingStatus.style.color = "#22c55e";
      localStorage.setItem("bookingDone", "true");
      paymentBtn.style.display = "block";
      loadBookings();
    } else {
      bookingStatus.textContent = res.message;
      bookingStatus.style.color = "red";
    }
  });
};

// --------------------------------------
// 6️⃣ LOAD BOOKINGS (UI ONLY)
// --------------------------------------
function loadBookings() {
  bookingList.innerHTML = `
    <p class="small-text">
      Booking created successfully. Proceed to payment.
    </p>
  `;
}

// --------------------------------------
// 7️⃣ PAYMENT BUTTON
// --------------------------------------
paymentBtn.onclick = function () {
  window.location.href = "payment.html";
};

// --------------------------------------
// 8️⃣ LOAD REVIEWS
// --------------------------------------
function loadReviews() {
  apiCall("get-reviews/").then(data => {
    reviewList.innerHTML = "";
    data.reviews?.forEach(r => {
      const stars = "★".repeat(r.rating) + "☆".repeat(5 - r.rating);
      reviewList.innerHTML += `
        <div class="review-item">
          <div class="review-stars">${stars}</div>
          <strong>${r.name}</strong>
          <p class="small-text">${r.text}</p>
        </div>`;
    });
  });
}

// --------------------------------------
// 9️⃣ ADD REVIEW
// --------------------------------------
reviewForm.onsubmit = function (e) {
  e.preventDefault();
  apiCall("reviews/", "POST", {
    name: reviewName.value,
    rating: reviewRating.value,
    text: reviewText.value
  }).then(() => {
    reviewForm.reset();
    loadReviews();
  });
};

// --------------------------------------
// 🔟 CONTACT FORM
// --------------------------------------
contactForm.onsubmit = function (e) {
  e.preventDefault();
  apiCall("contact/", "POST", {
    name: contactName.value,
    email: contactEmail.value,
    message: contactMessage.value
  }).then(res => contactResult.textContent = res.message);
};

// --------------------------------------
// 1️⃣1️⃣ NEWSLETTER
// --------------------------------------
newsletterForm.onsubmit = function (e) {
  e.preventDefault();
  apiCall("newsletter/", "POST", {
    email: newsletterEmail.value
  }).then(res => newsletterResult.textContent = res.message);
};

// --------------------------------------
// 1️⃣2️⃣ APP START (ONLY ONE ONLOAD)
// --------------------------------------
window.onload = function () {
  loadStations();
  loadBookings();
  loadReviews();

  if (navToggle) {
    navToggle.onclick = () => navLinks.classList.toggle("open");
  }
};
