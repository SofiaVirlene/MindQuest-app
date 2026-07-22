import java.util.Scanner;

class ContaBancaria {

    String numero;
    String titular;
    double saldo;
    double limiteMax;
    double limiteAtual;

    public ContaBancaria(String numero, String titular, double saldo, double limite) {
        this.numero = numero;
        this.titular = titular;
        this.saldo = saldo;
        this.limiteMax = limite;
        this.limiteAtual = limite;
    }

    public void saque(double valor, Scanner leitor) {
        double disponivel = this.saldo + this.limiteAtual;

        if (valor <= this.saldo) {
            this.saldo -= valor;
            System.out.println("[SUCESSO] Saque realizado direto do saldo.");
        } 
        else if (valor <= disponivel) {
            System.out.printf("Saldo insuficiente (R$%.2f). Deseja usar o limite? (s/n): ", this.saldo);
            String autoriza = leitor.next();

            if (autoriza.equalsIgnoreCase("s")) {
                this.saldo -= valor;
                this.limiteAtual = this.limiteMax + this.saldo; 
                System.out.println("[SUCESSO] Saque realizado utilizando o limite.");
            } else {
                System.out.println("[CANCELADO] Operação encerrada pelo usuário.");
            }
        } 
        else {
            System.out.println("[ERRO] Valor excede o saldo e o limite disponível.");
        }
    }

    public void deposito(double valor) {
        if (this.limiteAtual < this.limiteMax) {
            double faltandoParaLimite = this.limiteMax - this.limiteAtual;
            
            if (valor <= faltandoParaLimite) {
                this.limiteAtual += valor;
                this.saldo += valor;
            } else {
                this.limiteAtual = this.limiteMax;
                this.saldo += valor;
            }
        } else {
            this.saldo += valor;
        }
        System.out.println("[SUCESSO] Depósito processado.");
    }

    public void mostraStatus() {
        System.out.printf("Titular: %s | Saldo: R$%.2f | Limite: R$%.2f (Máx: R$%.2f)%n", 
                this.titular, this.saldo, this.limiteAtual, this.limiteMax);
    }
}

public class Principal {
    public static void main(String[] args) {
        Scanner leitor = new Scanner(System.in);

        ContaBancaria conta1 = new ContaBancaria("123-4", "João", 100.0, 500.0);

        System.out.println("--- BEM-VINDO AO BANCO JAVA ---");
        conta1.mostraStatus();

        System.out.print("\nDigite o valor do saque: R$ ");
        double valorSaque = leitor.nextDouble();
        conta1.saque(valorSaque, leitor);
        conta1.mostraStatus();

        System.out.print("\nDigite um valor para depósito: R$ ");
        double valorDeposito = leitor.nextDouble();
        conta1.deposito(valorDeposito);
        conta1.mostraStatus();

        leitor.close();
    }
}