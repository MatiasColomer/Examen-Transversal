document.addEventListener('DOMContentLoaded', () => {
    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    const addToCartButtons = document.querySelectorAll('.add-to-cart');
    if (addToCartButtons.length > 0) {
        addToCartButtons.forEach(button => {
            button.addEventListener('click', () => {
                const productId = button.getAttribute('data-id');
                const productName = button.getAttribute('data-name');
                const productPrice = parseFloat(button.getAttribute('data-price'));

                const product = cart.find(item => item.id === productId);
                if (product) {
                    product.quantity += 1;
                } else {
                    cart.push({ id: productId, name: productName, price: productPrice, quantity: 1 });
                }

                localStorage.setItem('cart', JSON.stringify(cart));
                updateCartDisplay();
            });
        });
    }

    const saveCartButton = document.getElementById('sendPurchaseButton');
    if (saveCartButton) {
        saveCartButton.addEventListener('click', (event) => {
            event.preventDefault();

            const csrftoken = getCookie('csrftoken');

            const customerName = document.getElementById('nombre').value.trim();
            const customerEmail = document.getElementById('email').value.trim();
            const customerAddress = document.getElementById('direccion').value.trim();
            const purchaseData = JSON.parse(localStorage.getItem('cart')) || [];

            if (!customerName || !customerEmail || purchaseData.length === 0) {
                alert('Por favor, complete todos los campos y asegúrese de que el carrito no esté vacío.');
                return;
            }

            const formData = {
                nombre: customerName,
                email: customerEmail,
                direccion: customerAddress,
                purchase_data: purchaseData  // No es necesario convertir a JSON
            };

            fetch('/save_purchase/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify(formData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    localStorage.removeItem('cart');
                    alert('¡Compra realizada exitosamente!');
                    updateCartDisplay();
                } else {
                    alert('Error al procesar la compra. Por favor, inténtelo de nuevo.');
                    console.error('Error del servidor:', data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al procesar la compra. Por favor, inténtelo de nuevo.');
            });
        });
    }

    function updateCartDisplay() {
        const cartDisplay = document.getElementById('cartDisplay');
        const totalPriceElement = document.getElementById('totalPrice');
        let totalPrice = 0;

        if (cartDisplay) {
            cartDisplay.innerHTML = '';
            cart.forEach(item => {
                const cartItem = document.createElement('li');
                cartItem.className = 'list-group-item';
                cartItem.textContent = `${item.name} - ${item.quantity} x $${item.price.toFixed(2)}`;

                const decreaseButton = document.createElement('button');
                decreaseButton.className = 'btn btn-danger btn-sm ml-2';
                decreaseButton.textContent = '-';
                decreaseButton.addEventListener('click', () => {
                    if (item.quantity > 1) {
                        item.quantity--;
                    } else {
                        cart = cart.filter(prod => prod.id !== item.id);
                    }
                    localStorage.setItem('cart', JSON.stringify(cart));
                    updateCartDisplay();
                });

                const removeAllButton = document.createElement('button');
                removeAllButton.className = 'btn btn-danger btn-sm';
                removeAllButton.textContent = 'Eliminar';
                removeAllButton.addEventListener('click', () => {
                    cart = cart.filter(prod => prod.id !== item.id);
                    localStorage.setItem('cart', JSON.stringify(cart));
                    updateCartDisplay();
                });

                const buttonContainer = document.createElement('div');
                buttonContainer.className = 'action-buttons';
                buttonContainer.appendChild(decreaseButton);
                buttonContainer.appendChild(removeAllButton);

                cartItem.appendChild(buttonContainer);
                cartDisplay.appendChild(cartItem);

                totalPrice += item.quantity * item.price;
            });

            if (totalPriceElement) {
                totalPriceElement.textContent = totalPrice.toFixed(2);
            }
        }
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    updateCartDisplay();
    
    fetch('https://mindicador.cl/api')
        .then(response => {
            if (!response.ok) {
                throw new Error('No se pudo obtener los indicadores económicos');
            }
            return response.json();
        })
        .then(data => {
            const carouselInner = document.getElementById('economicIndicators');
            if (carouselInner) {
                if (data && data.dolar && data.euro && data.bitcoin) {
                    const itemHtml = `
                        <div class="carousel-item active">
                            <h5>Dólar</h5>
                            <p>Valor: ${data.dolar.valor}</p>
                            <p>Unidad de Medida: ${data.dolar.unidad_medida}</p>
                        </div>
                        <div class="carousel-item">
                            <h5>Euro</h5>
                            <p>Valor: ${data.euro.valor}</p>
                            <p>Unidad de Medida: ${data.euro.unidad_medida}</p>
                        </div>
                        <div class="carousel-item">
                            <h5>Bitcoin</h5>
                            <p>Valor: ${data.bitcoin.valor}</p>
                            <p>Unidad de Medida: ${data.bitcoin.unidad_medida}</p>
                        </div>
                    `;
                    carouselInner.innerHTML = itemHtml;
                } else {
                    throw new Error('Formato de datos de indicadores económicos no válido');
                }
            }
        })
        .catch(error => console.error('Error al obtener indicadores:', error.message));
});
