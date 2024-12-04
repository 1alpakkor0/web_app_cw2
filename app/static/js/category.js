
document.addEventListener('DOMContentLoaded', function() {
    // Get the CSRF token from the meta tag
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // Handling the like button
    document.querySelectorAll('.like-btn').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;
            const likeButton = this;

            fetch('/like_product', {
                method: 'POST',
                credentials: 'include', // Include cookies for CSRF protection
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken 
                },
                body: JSON.stringify({ product_id: productId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'liked') {
                    this.textContent = 'Unlike';
                } else if (data.status === 'unliked') {
                    likeButton.textContent = 'Like';

                    // Removing the product card from the wishlist page
                    const currentUrl = window.location.pathname;
                    if (currentUrl == '/wishlist') {
                        const card = likeButton.closest('.col-md-4');
                        if (card) {
                            card.remove();
                        }
                    }
                } else {
                    alert('Error: ' + (data.message || 'Unknown error occurred.'));
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while updating the like status.');
            });
        });
    });

    // Handling the add to cart button
    document.querySelectorAll('.add-to-cart-btn').forEach(button => {
        button.addEventListener('click', function() {
            const productId = this.dataset.productId;

            fetch('/add_to_cart', {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken 
                },
                body: JSON.stringify({ product_id: productId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'added') {
                    // Updating the cart count in the navbar and showing an alert
                    const cartBadge = document.querySelector('.btn-success .badge');
                    if (cartBadge) {
                        cartBadge.textContent = data.cart_count;
                    }
                    alert('Product added to cart!');
                } else {
                    alert('Failed to add product to cart.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while adding the product to the cart.');
            });
        });
    });
});

