
document.addEventListener('DOMContentLoaded', () => {
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    document.querySelectorAll('.remove-from-cart-btn').forEach(button => {
        button.addEventListener('click', function() {
            const itemId = this.dataset.itemId;

            fetch('/remove_from_cart', {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({ item_id: itemId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'removed') {
                    // Removing the item row from the table
                    const row = document.getElementById(`cart-item-${itemId}`);
                    if (row) {
                        row.remove();
                    }
                    // Updating the cart count in the navbar
                    const cartBadge = document.querySelector('.btn-success .badge');
                    if (cartBadge) {
                        cartBadge.textContent = data.cart_count;
                    }

                    // Updating the total amount displayed
                    const totalElement = document.getElementById('cart-total');
                    if (totalElement) {
                        totalElement.textContent = '$' + data.total_amount.toFixed(2);
                    }

                    alert('Item removed from cart!');
                } else {
                    alert(data.message || 'Failed to remove item from cart.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while removing the item from the cart.');
            });
        });
    });
});

