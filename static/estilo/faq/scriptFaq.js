// Alternar entre categorias
document.querySelectorAll('.category-btn').forEach(button => {
    button.addEventListener('click', () => {
        // Remover classe ativa de todos os botões
        document.querySelectorAll('.category-btn').forEach(btn => {
            btn.classList.remove('active');
        });

        // Adicionar classe ativa ao botão clicado
        button.classList.add('active');

        // Ocultar todas as seções
        document.querySelectorAll('.faq-section').forEach(section => {
            section.classList.remove('active');
        });

        // Mostrar a seção correspondente
        const category = button.getAttribute('data-category');
        document.getElementById(category).classList.add('active');
    });
});

// Alternar perguntas e respostas
document.querySelectorAll('.faq-question').forEach(question => {
    question.addEventListener('click', () => {
        const item = question.parentElement;
        item.classList.toggle('active');
    });
});
