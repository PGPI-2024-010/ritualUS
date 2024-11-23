document.addEventListener("DOMContentLoaded", function() {
    let quantityInput = document.getElementById('quantity');
    let addToCartBtn = document.getElementById('addToCartBtn');
    let quantityError = document.getElementById('quantity-error');

    // Verificar si el botón existe
    if (!addToCartBtn) return; 

    // Obtener el valor de data-max-stock desde el atributo del input
    let maxStock = parseInt(quantityInput.getAttribute('data-max-stock'));
    let addToCartUrl = addToCartBtn.getAttribute('data-add-to-cart-url');

    function validateQuantity() {
        let quantity = quantityInput.value
        console.log(quantity)
        if (isNaN(quantity) || quantity < 1 || quantity > maxStock || !Number.isInteger(Number(quantity))) {
            // Si la cantidad es inválida, deshabilitamos el botón de agregar al carrito
            quantityError.style.display = 'block'; 
            addToCartBtn.classList.add('disabled');
            addToCartBtn.href = "javascript:void(0);"; // Evitamos que sea clicable
        } else {
            // Si es válida, habilitamos el botón
            quantityError.style.display = 'none';
            addToCartBtn.classList.remove('disabled');
            addToCartBtn.href = addToCartUrl; // Volvemos a habilitar el enlace
        }
    }

    // Llamamos a la función cada vez que cambia el valor del input
    quantityInput.addEventListener('input', function() {
        // Aseguramos que el valor ingresado sea un número entero
        quantityInput.value = Math.floor(quantityInput.value);
        validateQuantity();
    });
    // Validar inmediatamente cuando se carga la página por si se modifica el valor
    validateQuantity();
});
