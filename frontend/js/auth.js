function register() {
  fetch(API_BASE + "register/", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      username: username.value,
      email: email.value,
      password: password.value
    })
  })
  .then(res => res.json())
  .then(() => {
    alert("Registration Successful");
    window.location = "login.html";
  });
}


function login() {
  fetch(API_BASE + "accounts/login/", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      username: username.value,
      password: password.value
    })
  })
  .then(res => res.json())
  .then(data => {
    localStorage.setItem("access", data.access);
    localStorage.setItem("refresh", data.refresh);
    window.location = "stations.html";
  });
}
