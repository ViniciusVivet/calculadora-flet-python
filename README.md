# 🚀 Calculadora Flet Avançada 📊

<img width="325" height="531" alt="Captura de Tela (117)" src="https://github.com/user-attachments/assets/10d6c542-4775-4df8-8e87-49524782f360" />


## ✨ Visão Geral do Projeto

Uma calculadora moderna e funcional, desenvolvida integralmente em **Python** utilizando o framework **Flet**. Este projeto demonstra a capacidade de construir interfaces gráficas (GUI) ricas e responsivas com uma única base de código Python, abstraindo a complexidade do desenvolvimento Front-End.

É uma ferramenta simples, porém robusta, para realizar operações matemáticas básicas, com foco na experiência do usuário e na clareza da interface.

## 🌟 Funcionalidades Implementadas

* **Operações Básicas:** Adição, subtração, multiplicação, divisão e porcentagem.
* **Entrada de Dados Flexível:** Suporte tanto para cliques nos botões da interface quanto para entrada via **teclado numérico e de símbolos**.
* **Gerenciamento de Display:** Limpeza total (`AC`), remoção de último caractere (`DEL`).
* **Interface Intuitiva:** Layout de botões claro e display de resultado centralizado.
* **Feedback Visual:** Efeitos de hover nos botões para melhorar a usabilidade.
* **Histórico de Operações:** Exibe a última expressão calculada acima do resultado principal.

## 🛠️ Tecnologias Utilizadas

* **Python:** Linguagem de programação principal.
* **Flet:** Framework Python para construção de UI (Interface de Usuário) multiplataforma.

## 🚀 Como Usar e Rodar o Projeto

Para testar a calculadora em seu ambiente local, siga os passos abaixo:

1.  **Pré-requisitos:**
    * Certifique-se de ter o [Python 3.x](https://www.python.org/downloads/) instalado em sua máquina.
    * Instale o `flet` e suas ferramentas de linha de comando (`flet-cli`) via pip:
        ```bash
        py -m pip install flet flet-cli
        ```
        *(Se você encontrar problemas com `flet` não sendo reconhecido, pode ser necessário adicionar a pasta `Scripts` da sua instalação Python ao PATH do sistema operacional e reiniciar o terminal/VS Code.)*

2.  **Clone o Repositório:**
    ```bash
     git clone [https://github.com/ViniciusVivet/calculadora-flet-python.git](https://github.com/ViniciusVivet/calculadora-flet-python.git)
    ```
   
3.  **Navegue até a Pasta do Projeto:**
    ```bash
    cd calculadora-flet-python
    ```

4.  **Execute a Aplicação:**
    * Para rodar a calculadora como **aplicativo de desktop (com hot reload)**:
        ```bash
        flet run calculadora.py 
        # Ou 'py -m flet run calculadora.py' se 'flet' não for reconhecido diretamente
        ```
    * Para rodar a calculadora em uma **aba do navegador (com hot reload)**:
        ```bash
        flet run calculadora.py --web
        # Ou 'py -m flet run calculadora.py --web'
        ```
## 🛣️ Próximos Passos (Melhorias Futuras)

* Adicionar operações científicas (seno, cosseno, raiz quadrada).
* Implementar um histórico de cálculos detalhado.
* Suporte para múltiplos temas (claro/escuro).
* Otimização para diferentes tamanhos de tela (responsividade avançada).

## 🧑‍💻 Autor

**Douglas Vinicius Alves da Silva**
* [**Meu Perfil no GitHub**](https://github.com/ViniciusVivet)
* [**Meu Perfil no LinkedIn**](https://www.linkedin.com/in/vivetsp/)
* **Email:** [douglasvivet@gmail.com](mailto:douglasvivet@gmail.com)
