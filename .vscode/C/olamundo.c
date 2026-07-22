#include <stdio.h>

int main() {
    printf("Ola mundo");
    return 0;
}

// #include <stdio.h>

// int main() {
//     int a, b, soma;
//     printf("Primeiro numero: ");
//     scanf("%d", &a);
//     printf("Segundo numero: ");
//     scanf("%d", &b);

//     soma = a + b;
//     printf("Soma: %d\n", soma);

// if (soma > 10) {
//     printf("A soma e maior que 10\n");
// } else {
//     printf("A soma e menor ou igual a 10\n");}
//     return 0;
// }

// #include <stdio.h>

// int main() {
//     int n;
//     printf("Digite um numero: ");
//     scanf("%d", &n);

//     if (n % 2 == 0) {
//         printf("O numero e par\n");
//     } else {
//         printf("O numero e impar\n");
//     }
//     return 0;
// }

// #include <stdio.h>

// int main() {
//     float nota;
//     printf("Digite a nota do aluno: ");
//     scanf("%f", &nota);

//     if (nota >= 7.0) {
//         printf("Aprovado\n");
//     } else if (nota >= 4.0) {
//         printf("Recuperacao\n");
//     } else {
//         printf("Reprovado\n");
//     }
//     return 0;
// }

// #include <stdio.h>

// int main() {
//     int velocidade, limite;
//     printf("Digite a velocidade do veiculo: ");
//     scanf("%d", &velocidade);
//     printf("Digite o limite da via: ");
//     scanf("%d", &limite);

//     if (velocidade > limite) {
//         printf("Multa! Velocidade acima do limite\n");
//     } else {
//         printf("Velocidade dentro do limite. Boa!\n");
//     }
//     return 0;
// }

// #include <stdio.h>

// int main() {
    // float nota;
    // int freaquencia;
    // printf("Digite a nota do aluno: ");
    // scanf("%f", &nota);
//     printf("Digite a frequencia do aluno (em porcentagem): ");
//     scanf("%d", &freaquencia);

//     if (nota >= 7.0 && freaquencia >= 75) {
//         printf("Aprovado\n");
//     } else if (nota >= 4.0 && freaquencia >= 75) {
//         printf("Recuperacao\n");
//     } else {
//         printf("Reprovado\n");
//     }
//     return 0;
// }

// #include <stdio.h>
// int main() {
//     float saldo, saque;
//     printf("Saldo atual: ");
//     scanf("%f", &saldo);
//     printf("Valor do saque: ");
//     scanf("%f", &saque);

//     if (saldo >= saque) {
//         saldo = saldo - saque;
//         printf("Saque realizado com sucesso! Saldo restante: %.2f\n", saldo);
//     } else {
//         printf("Saldo insuficiente para realizar o saque.\n");
//     }
//     return 0;
// }