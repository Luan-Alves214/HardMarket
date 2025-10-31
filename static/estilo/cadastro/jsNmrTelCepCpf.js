document.addEventListener('DOMContentLoaded', function() {
    const celularInput = document.getElementById('celular');
    const cpfInput = document.getElementById('cpf');
    const cepInput = document.getElementById('cep');

    // Formatação do Celular
    celularInput.addEventListener('input', function(e) {
        // Remove tudo que não é número
        let value = e.target.value.replace(/\D/g, '');

        // Aplica a formatação
        if (value.length > 0) {
            // Formato: (00) 00000-0000
            if (value.length <= 2) {
                value = '(' + value;
            } else if (value.length <= 7) {
                value = '(' + value.substring(0, 2) + ') ' + value.substring(2);
            } else if (value.length <= 11) {
                value = '(' + value.substring(0, 2) + ') ' + value.substring(2, 7) + '-' + value.substring(7);
            } else {
                // Limita a 11 dígitos (formato completo)
                value = '(' + value.substring(0, 2) + ') ' + value.substring(2, 7) + '-' + value.substring(7, 11);
            }
        }

        e.target.value = value;
    });

    // Formatação do CPF
    cpfInput.addEventListener('input', function(e) {
        // Remove tudo que não é número
        let value = e.target.value.replace(/\D/g, '');

        // Aplica a formatação
        if (value.length > 0) {
            // Formato: 000.000.000-00
            if (value.length <= 3) {
                value = value;
            } else if (value.length <= 6) {
                value = value.substring(0, 3) + '.' + value.substring(3);
            } else if (value.length <= 9) {
                value = value.substring(0, 3) + '.' + value.substring(3, 6) + '.' + value.substring(6);
            } else if (value.length <= 11) {
                value = value.substring(0, 3) + '.' + value.substring(3, 6) + '.' + value.substring(6, 9) + '-' + value.substring(9);
            } else {
                // Limita a 11 dígitos (formato completo)
                value = value.substring(0, 3) + '.' + value.substring(3, 6) + '.' + value.substring(6, 9) + '-' + value.substring(9, 11);
            }
        }

        e.target.value = value;
    });

    // Formatação do CEP
    cepInput.addEventListener('input', function(e) {
        // Remove tudo que não é número
        let value = e.target.value.replace(/\D/g, '');

        // Aplica a formatação
        if (value.length > 0) {
            // Formato: 00000-000
            if (value.length <= 5) {
                value = value;
            } else if (value.length <= 8) {
                value = value.substring(0, 5) + '-' + value.substring(5);
            } else {
                // Limita a 8 dígitos (formato completo)
                value = value.substring(0, 5) + '-' + value.substring(5, 8);
            }
        }

        e.target.value = value;
    });

    // Permite navegação com teclado dentro dos campos formatados
    function allowKeyboardNavigation(input) {
        input.addEventListener('keydown', function(e) {
            // Permite: Backspace, Delete, Tab, Escape, Enter, setas
            if ([8, 9, 13, 27, 46, 37, 38, 39, 40].indexOf(e.keyCode) !== -1) {
                return;
            }

            // Permite apenas números
            if ((e.keyCode < 48 || e.keyCode > 57) && (e.keyCode < 96 || e.keyCode > 105)) {
                e.preventDefault();
            }
        });
    }

    allowKeyboardNavigation(celularInput);
    allowKeyboardNavigation(cpfInput);
    allowKeyboardNavigation(cepInput);
});