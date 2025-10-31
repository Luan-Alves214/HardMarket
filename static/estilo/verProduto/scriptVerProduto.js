    function toggleFavorite2(element) {
        const heartIcon2 = element.querySelector('.heart-icon2');

        // Alterna entre os estados
        if (heartIcon2.classList.contains('empty')) {
            heartIcon2.classList.remove('empty');
            heartIcon2.classList.add('filled');
            console.log('Produto favoritado!');
        } else {
            heartIcon2.classList.remove('filled');
            heartIcon2.classList.add('empty');
            console.log('Produto desfavoritado!');
        }
    }

    // Inicialização - verificar se há favoritos salvos
    document.addEventListener('DOMContentLoaded', function () {
        // Aqui você pode adicionar lógica para carregar favoritos salvos
        // Por exemplo, de localStorage
    });