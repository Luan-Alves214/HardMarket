document.addEventListener('DOMContentLoaded', function() {
    const areaUpload = document.getElementById('area-upload');
    const inputUpload = document.getElementById('upload-imagem');
    const previewImagem = document.getElementById('preview-imagem');
    const infoImagem = document.getElementById('info-imagem');
    const botaoTrocar = document.getElementById('botao-trocar');

    // Função para exibir a imagem
    function exibirImagem(file) {
        if (file && file.type.startsWith('image/')) {
            const reader = new FileReader();

            reader.onload = function(e) {
                previewImagem.src = e.target.result;

                // Adiciona classe para mostrar a imagem
                areaUpload.classList.add('com-imagem');

                // Mostra informações da imagem
                const tamanhoKB = Math.round(file.size / 1024);
                infoImagem.textContent = `${file.name} (${tamanhoKB} KB)`;
            }

            reader.readAsDataURL(file);
        }
    }

    // Upload por clique
    inputUpload.addEventListener('change', function(e) {
        if (this.files && this.files[0]) {
            exibirImagem(this.files[0]);
        }
    });

    // Upload por drag & drop
    areaUpload.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.style.backgroundColor = '#dee2e6';
        this.style.borderColor = '#0d6efd';
    });

    areaUpload.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.style.backgroundColor = '#f8f9fa';
        this.style.borderColor = '#6c757d';
    });

    areaUpload.addEventListener('drop', function(e) {
        e.preventDefault();
        this.style.backgroundColor = '#f8f9fa';
        this.style.borderColor = '#6c757d';

        if (e.dataTransfer.files.length) {
            const file = e.dataTransfer.files[0];
            exibirImagem(file);
            inputUpload.files = e.dataTransfer.files;
        }
    });

    // Botão para trocar imagem
    botaoTrocar.addEventListener('click', function(e) {
        e.stopPropagation(); // Impede que o clique no botão abra o seletor de arquivos
        inputUpload.click();
    });

    // Permite clicar na área para trocar a imagem (mesmo quando já tem uma imagem)
    areaUpload.addEventListener('click', function() {
        inputUpload.click();
    });
});