document.addEventListener('DOMContentLoaded', function () {
    //const buyNowButtons = document.querySelectorAll('.buy-now-btn');
    const buyNowButtons = document.querySelectorAll('.buy-now-btn');

    buyNowButtons.forEach(buyNowButton => {
	    
	    //alert('attaching click event');
            const productId = buyNowButton.getAttribute('data-product-id');
            const modal = document.querySelectorAll('#buyModal'+productId);
            const quantityError = document.querySelector('#quantityError');
            const uname = buyNowButton.getAttribute('data-user-id');
            const quantityInput = document.querySelector('#quantity'+productId);
            const rateString = buyNowButton.getAttribute('data-product-rate'+productId);
            const rate = parseFloat(rateString);
            const totalPriceInput = document.querySelector('#totalPrice'+productId);
            const updateTotalPrice = () => {
                const quantity = parseInt(quantityInput.value);
                const total = rate * quantity;
                totalPriceInput.value = `Rs.${total.toFixed(2)}`;
            };
            quantityInput.addEventListener('input', updateTotalPrice);
        buyNowButton.addEventListener('click', function () {
		//alert('attaching click handler');
            //const modal = buyNowButton.closest('.modal')
            // quantityError.textContent = '';
            // totalPriceInput.value = '';

            // Add an input event listener to the quantity input

            if (parseInt(quantityInput.value) > parseInt(quantityInput.max)) {
                quantityError.textContent = 'Quantity exceeds available quantity';
            } else if (parseInt(quantityInput.value) <= 0) {
                quantityError.textContent = 'Quantity must be greater than 0';
            } else {
                // Update the database with the new quantity
                const url = `/buy_product/${uname}/${productId}/${quantityInput.value}`;
                fetch(url, {
                    method: 'POST',
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            const closeButton = document.querySelector('[data-bs-dismiss="modal"]');
                            closeButton.click();
                            window.location.reload();
                        } else {
                            console.error('Failed to update quantity');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            }
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');

    addToCartButtons.forEach(addToCartButton => {
        addToCartButton.addEventListener('click', function () {
            const container = addToCartButton.closest('.card-footer').querySelector('.add-to-cart-container');
            container.style.display = 'block';

            const cartQuantityInput = container.querySelector('#cartQuantity');
            const cartTotalPriceInput = container.querySelector('#cartTotalPrice');
            const cartQuantityError = container.querySelector('#cartQuantityError');
            const productId = addToCartButton.getAttribute('data-product-id');
            const rateString = addToCartButton.getAttribute('data-product-rate');
            const rate = parseFloat(rateString);
            const userId = addToCartButton.getAttribute('data-user-id');
            console.log(userId)
            cartQuantityError.textContent = '';
            cartTotalPriceInput.value = '';

            // Function to update the total price for cart
            const updateCartTotalPrice = () => {
                const quantity = parseInt(cartQuantityInput.value);
                const total = rate * quantity;
                cartTotalPriceInput.value = `Rs.${total.toFixed(2)}`;
            };

            // Add an input event listener to the cart quantity input
            cartQuantityInput.addEventListener('input', updateCartTotalPrice);

            const confirmCartButton = container.querySelector('.confirm-add-to-cart-btn');
            confirmCartButton.addEventListener('click', function () {
                if (parseInt(cartQuantityInput.value) > parseInt(cartQuantityInput.max)) {
                    cartQuantityError.textContent = 'Quantity exceeds available quantity';
                } else if (parseInt(cartQuantityInput.value) <= 0) {
                    cartQuantityError.textContent = 'Quantity must be greater than 0';
                } else {
                    // Send the request to add to cart
                    
                    const url = `/add_to_cart/${userId}/${productId}/${cartQuantityInput.value}`;                    fetch(url, {
                        method: 'POST',
                    })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                console.log('Added to cart:', productId);
                                container.style.display = 'none'; // Hide the container
                            } else {
                                console.error('Failed to add to cart');
                            }
                        })
                        .catch(error => {
                            console.error('Error:', error);
                        });                }
            });
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const checkoutButton = document.querySelector('.checkout-btn');
    checkoutButton.addEventListener('click', function () {
        const cartItems = document.querySelectorAll('.cart-item');
        const cartItemsData = [];
        const USER_ID = checkoutButton.getAttribute('data-user-id')

        cartItems.forEach(cartItem => {
            const productId = cartItem.getAttribute('data-product-id');
            const quantity = cartItem.getAttribute('data-quantity');
            cartItemsData.push({ productId, quantity });
        });

        // Send a request to the new checkout endpoint with cart items data
        fetch(`/checkout/${USER_ID}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(cartItemsData)
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
			//alert(data.goto);
			window.location.href=data.goto;
                    // Handle successful checkout, e.g., clear the cart or update UI
                } else {
                    console.error('Failed to complete checkout:', data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const removeFromCartButtons = document.querySelectorAll('.remove-from-cart-btn');
    
    removeFromCartButtons.forEach(removeButton => {
        removeButton.addEventListener('click', function () {
            const item_id = removeButton.getAttribute('data-item-id');
            const USER_ID = removeButton.getAttribute('data-user-id')

            // Send a POST request to remove_cart_item endpoint
            fetch(`/remove_cart_item/${USER_ID}/${item_id}`, {
                method: 'POST',
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Refresh the page after successful removal
                        window.location.reload();
                    } else {
                        console.error('Failed to remove item from cart');
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                });
        });
    });
});
