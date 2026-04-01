// Dummy Review Section (replace with dynamic version using add_review.html)
document.addEventListener('DOMContentLoaded', () => {
    // Initialize character counter if review form exists
    const reviewText = document.getElementById('review-text');
    const charCount = document.querySelector('.char-count');
    
    if (reviewText && charCount) {
        reviewText.addEventListener('input', () => {
            const length = reviewText.value.length;
            charCount.textContent = `${length}/1000 characters`;
        });
    }
});

// Toggle the review form visibility
function toggleReviewForm() {
    const showFormSection = document.getElementById('show-form-section');
    const formContainer = document.getElementById('review-form-container');
    const showFormBtn = document.getElementById('show-review-form-btn');
    
    if (formContainer.style.display === 'none' || formContainer.style.display === '') {
        // Show the form, hide the button
        formContainer.style.display = 'block';
        showFormSection.style.display = 'none';
        // Scroll to form
        formContainer.scrollIntoView({ behavior: 'smooth' });
    } else {
        // Hide the form, show the button
        formContainer.style.display = 'none';
        showFormSection.style.display = 'block';
        // Clear form when hiding
        const form = document.getElementById('review-form');
        if (form) {
            form.reset();
            const charCount = document.querySelector('.char-count');
            if (charCount) {
                charCount.textContent = '0/1000 characters';
            }
        }
    }
}