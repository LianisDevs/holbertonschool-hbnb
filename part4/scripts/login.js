document.addEventListener("DOMContentLoaded", () => {
  const loginSection = document.getElementById("login-section");
  const signupSection = document.getElementById("signup-section");

  // Toggle: Login → Sign Up 
  document.getElementById("goToSignup").addEventListener("click", () => {
    loginSection.style.display = "none";
    signupSection.style.display = "block"; 
  });

  //Toggle: Sign Up → Login 
  document.getElementById("goToLogin").addEventListener("click", () => {
    signupSection.style.display = "none";
    loginSection.style.display = "block"; 
  });

  // Login submit 
  const loginForm = document.getElementById("login-form");

  if (loginForm) {
    loginForm.addEventListener("submit", async (event) => {
      event.preventDefault();

      const formData = new FormData(event.target);
      const email = formData.get("email");
      const password = formData.get("password");

      await loginUser(email, password);
    });
  }

  async function loginUser(email, password) {
    const response = await fetch("http://127.0.0.1:5000/api/v1/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, password }),
    });

    if (response.ok) {
      const data = await response.json();
      document.cookie = `token=${data.access_token}; path=/`;
      window.location.href = "index.html";
    } else {
      alert("Login failed: " + response.statusText);
    }
  }

  // Sign Up submit
  const signupForm = document.getElementById("signup-form");

  if (signupForm) {
    signupForm.addEventListener("submit", async (event) => {
      event.preventDefault();

      const formData = new FormData(event.target);
      const first_name = formData.get("firstName");
      const last_name = formData.get("lastName");
      const email = formData.get("signupEmail");
      const password = formData.get("signupPassword");

      await signUpUser(first_name, last_name, email, password);
    });
  }

  async function signUpUser(first_name, last_name, email, password) {
    const response = await fetch("http://127.0.0.1:5000/api/v1/users/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ first_name, last_name, email, password }),
    });

    if (response.ok) {
      alert("Account created! Please sign in.");
      signupForm.reset();
      signupSection.style.display = "none";
      loginSection.style.display = "block";
    } else {
      alert("Sign up failed: " + response.statusText);
    }
  }
});
