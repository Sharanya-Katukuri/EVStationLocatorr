const API_BASE = "https://evstationlocator.onrender.com/api/";

function getToken() {
  return localStorage.getItem("access");
}

function authHeader() {
  return {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + getToken()
  };
}

function logout() {
  localStorage.clear();
  window.location = "login.html";
}