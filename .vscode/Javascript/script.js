// 1. Pegamos o botão do HTML pelo ID
const botao = document.getElementById("meuBotao");

// 2. Criamos uma função que será executada ao clicar
botao.addEventListener("click", function() {
    alert("Você clicou no botão! O JavaScript está funcionando.");
    document.body.style.backgroundColor = "lightblue";
});

// 1. Criamos uma variável para guardar o número de likes (começa em 0)
let likes = 0;

// 2. Pegamos os elementos do HTML
const botao = document.getElementById("botaoLike");
const displayContador = document.getElementById("contador");

// 3. Criamos o "ouvidor" de cliques
botao.addEventListener("click", function() {
    // Aumenta o número de likes em 1
    likes = likes + 1;
    
    // Atualiza o texto que aparece na tela
    displayContador.innerText = likes;

    // Um toque de estilo: muda a cor do botão quando clicado
    botao.style.backgroundColor = "#1877f2"; // Azul do Facebook
    botao.style.color = "white";
});