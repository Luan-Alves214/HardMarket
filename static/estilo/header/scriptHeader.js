document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.createElement('button');
    menuToggle.className = 'menu-toggle';
    menuToggle.innerHTML = '<span></span><span></span><span></span>';
    menuToggle.setAttribute('aria-label', 'Abrir menu');

    const menu = document.querySelector('.menu');
    const header = document.querySelector('.header');

    // Insere o botão hamburguer no header
    header.appendChild(menuToggle);

    menuToggle.addEventListener('click', function() {
        menu.classList.toggle('active');
        this.setAttribute('aria-expanded', menu.classList.contains('active'));
    });

    // Fecha o menu ao clicar em um link
    document.querySelectorAll('.menu a').forEach(link => {
        link.addEventListener('click', () => {
            menu.classList.remove('active');
            menuToggle.setAttribute('aria-expanded', 'false');
        });
    });
});