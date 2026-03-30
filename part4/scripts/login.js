document.addEventListener('DOMContentLoaded', () => {
	const loginForm = document.getElementById('login-form');

	if (loginForm) {
		loginForm.addEventListener('submit', async (event) => {
			event.preventDefault();

			const formData = new FormData(event.target);

			const email = formData.get("email");
			const password = formData.get("password");

			loginUser(email, password)

			async function loginUser(email, password) {
				const response = await fetch('http://127.0.0.1:5000/api/v1/auth/login', {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json',
						'Access-Control-Allow-Origin': '*'
					},
					body: JSON.stringify({ email, password })
				});
				if (response.ok) {
					const data = await response.json();
					document.cookie = `token=${data.access_token}; path=/`;
					window.location.href = 'index.html';
				} else {
					alert('Login failed: ' + response.statusText);
				}
			}
		});
	}
});

