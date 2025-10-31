function toggleFavorite(element) {
        const heartIcon = element.querySelector('.heart-icon');

        // Alterna entre os estados
        if (heartIcon.classList.contains('empty')) {
            heartIcon.classList.remove('empty');
            heartIcon.classList.add('filled');
            console.log('Produto favoritado!');
        } else {
            heartIcon.classList.remove('filled');
            heartIcon.classList.add('empty');
            console.log('Produto desfavoritado!');
        }
    }

    // Inicialização - verificar se há favoritos salvos
    document.addEventListener('DOMContentLoaded', function() {
        // Aqui você pode adicionar lógica para carregar favoritos salvos
        // Por exemplo, de localStorage
    });