import tkinter as tk
from tkinter import messagebox
import math
import locale

# Definir locale para português brasileiro
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
    except:
        pass


class Calculadora:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Calculadora com Histórico")
        self.root.geometry("400x600")
        self.root.minsize(350, 500)
        self.root.resizable(True, True)
        self.root.configure(bg='#4a4a4a')

        # Variáveis para armazenar a expressão e resultado
        self.expressao = ""
        self.expressao_calculada = ""  # Para armazenar a expressão sem formatação
        self.resultado_var = tk.StringVar()
        self.resultado_var.set("0")
        self.historico = []
        self.historico_visivel = False

        self.criar_interface()

    def criar_interface(self):
        # Container principal
        main_frame = tk.Frame(self.root, bg='#4a4a4a')
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Frame da calculadora (sempre visível)
        self.frame_calc = tk.Frame(main_frame, bg='#4a4a4a')
        self.frame_calc.pack(side='left', fill='both', expand=True)

        # Botão para mostrar/ocultar histórico
        frame_controle = tk.Frame(self.frame_calc, bg='#4a4a4a')
        frame_controle.pack(fill='x', pady=(0, 10))

        self.btn_historico = tk.Button(
            frame_controle,
            text="📋 Mostrar Histórico",
            font=('Arial', 10),
            bg='#4a4a4a',
            fg='white',
            bd=0,
            command=self.toggle_historico
        )
        self.btn_historico.pack(side='right')

        # Display da calculadora
        frame_display = tk.Frame(self.frame_calc, bg='#4a4a4a')
        frame_display.pack(pady=(0, 20), fill='x')

        self.display = tk.Entry(
            frame_display,
            textvariable=self.resultado_var,
            font=('Arial', 24, 'bold'),
            justify='right',
            state='readonly',
            bg='#4a4a4a',
            fg='black',
            bd=0,
            highlightthickness=2,
            highlightcolor='#4a4a4a'
        )
        self.display.pack(fill='x', ipady=10)

        # Frame para os botões
        frame_botoes = tk.Frame(self.frame_calc, bg='#4a4a4a')
        frame_botoes.pack(fill='both', expand=True)

        # Definindo os botões
        botoes = [
            ['C', 'X', '√', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['+/-', '0', '.', '=']
        ]

        # Criando os botões
        for i, linha in enumerate(botoes):
            for j, texto in enumerate(linha):
                self.criar_botao(frame_botoes, texto, i, j)

        # Frame do histórico (inicialmente oculto)
        self.frame_historico = tk.Frame(main_frame, bg='#4a4a4a')

        tk.Label(
            self.frame_historico,
            text="Histórico",
            font=('Arial', 14, 'bold'),
            bg='#4a4a4a',
            fg='black'
        ).pack(pady=(0, 10))

        # Lista do histórico com scrollbar
        frame_lista = tk.Frame(self.frame_historico, bg='#4a4a4a')
        frame_lista.pack(fill='both', expand=True)

        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side='right', fill='y')

        self.lista_historico = tk.Listbox(
            frame_lista,
            font=('Arial', 10),
            bg='#4a4a4a',
            fg='white',
            selectbackground='#4a4a4a',
            yscrollcommand=scrollbar.set,
            width=25
        )
        self.lista_historico.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.lista_historico.yview)

        # Botão para limpar histórico
        tk.Button(
            self.frame_historico,
            text="Limpar Histórico",
            font=('Arial', 10),
            bg='#e74c3c',
            fg='white',
            bd=0,
            command=self.limpar_historico
        ).pack(pady=(10, 0), fill='x')

    def formatar_numero(self, numero):
        """Formata número para o padrão brasileiro (1.000,00)"""
        try:
            # Converter para float se for string
            if isinstance(numero, str):
                numero = float(numero.replace('.', '').replace(',', '.'))

            # Se for número inteiro, não mostra casas decimais
            if isinstance(numero, float) and numero.is_integer():
                numero = int(numero)
                return f"{numero:,.0f}".replace(',', '.')
            else:
                # Formatar com 2 casas decimais
                formatado = f"{numero:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                return formatado
        except:
            return str(numero)

    def criar_botao(self, parent, texto, linha, coluna):
        # Definindo cores dos botões
        if texto in ['=']:
            cor_fundo = '#e74c3c'
            cor_texto = 'white'
        elif texto in ['C', 'X', '√', '+/-']:
            cor_fundo = '#95a5a6'
            cor_texto = 'black'
        elif texto in ['/', '*', '-', '+']:
            cor_fundo = '#f39c12'
            cor_texto = 'white'
        else:
            cor_fundo = '#34495e'
            cor_texto = 'white'

        botao = tk.Button(
            parent,
            text=texto,
            font=('Arial', 18, 'bold'),
            bg=cor_fundo,
            fg=cor_texto,
            bd=0,
            activebackground='#3498db',
            activeforeground='white',
            command=lambda t=texto: self.ao_clicar_botao(t)
        )

        botao.grid(
            row=linha,
            column=coluna,
            sticky='nsew',
            padx=2,
            pady=2
        )

        # Configurando o grid para expandir
        parent.grid_rowconfigure(linha, weight=1)
        parent.grid_columnconfigure(coluna, weight=1)

    def ao_clicar_botao(self, texto):
        try:
            if texto == 'C':
                self.limpar()
            elif texto == 'X':
                self.apagar()
            elif texto == '=':
                self.calcular()
            elif texto == '√':
                self.raiz_quadrada()
            elif texto == '+/-':
                self.trocar_sinal()
            else:
                self.adicionar_caractere(texto)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro inesperado: {str(e)}")
            self.limpar()

    def adicionar_caractere(self, char):
        # Substituir vírgula por ponto para compatibilidade
        if char == ',':
            char = '.'

        if self.resultado_var.get() == "0" and char.isdigit():
            self.expressao_calculada = char
            self.expressao = char
        else:
            self.expressao_calculada += char  # Versão para cálculo
            self.expressao += char

        self.atualizar_display()

    def limpar(self):
        self.expressao = ""
        self.expressao_calculada = ""
        self.resultado_var.set("0")

    def apagar(self):
        if self.expressao:
            self.expressao = self.expressao[:-1]
            self.expressao_calculada = self.expressao_calculada[:-1]
            if not self.expressao:
                self.resultado_var.set("0")
            else:
                self.atualizar_display()

    def atualizar_display(self):
        if self.expressao:
            # Tentar formatar números na expressão
            try:
                # Dividir por operadores mantendo-os
                import re
                partes = re.split(r'([+\-*/])', self.expressao)
                expressao_formatada = ""

                for parte in partes:
                    if parte.strip() and parte not in ['+', '-', '*', '/']:
                        try:
                            # Se for um número, formatar
                            numero = float(parte)
                            expressao_formatada += self.formatar_numero(numero)
                        except:
                            expressao_formatada += parte
                    else:
                        expressao_formatada += parte

                self.resultado_var.set(expressao_formatada)
            except:
                self.resultado_var.set(self.expressao)
        else:
            self.resultado_var.set("0")

    def calcular(self):
        try:
            if self.expressao_calculada:
                # Usar a expressão sem formatação para cálculo
                expressao_eval = self.expressao_calculada.replace('×', '*').replace('÷', '/')
                resultado = eval(expressao_eval)

                # Formatando o resultado
                if isinstance(resultado, float):
                    if resultado.is_integer():
                        resultado = int(resultado)
                    else:
                        resultado = round(resultado, 2)

                # Adicionando ao histórico com formatação brasileira
                expressao_historico = self.expressao.replace('*', '×').replace('/', '÷')
                resultado_formatado = self.formatar_numero(resultado)
                calculo_str = f"{expressao_historico} = {resultado_formatado}"
                self.historico.append(calculo_str)
                self.atualizar_lista_historico()

                # Mostrar resultado formatado
                resultado_str = self.formatar_numero(resultado)
                self.resultado_var.set(resultado_str)
                self.expressao = str(resultado)
                self.expressao_calculada = str(resultado)
        except ZeroDivisionError:
            messagebox.showerror("Erro", "Divisão por zero não é permitida!")
            self.limpar()
        except:
            messagebox.showerror("Erro", "Expressão inválida!")
            self.limpar()

    def raiz_quadrada(self):
        try:
            if self.expressao_calculada:
                numero = float(self.expressao_calculada)
                if numero < 0:
                    messagebox.showerror("Erro", "Não é possível calcular raiz quadrada de número negativo!")
                    return
                resultado = math.sqrt(numero)
                if resultado.is_integer():
                    resultado = int(resultado)
                else:
                    resultado = round(resultado, 2)

                # Adicionando ao histórico com formatação brasileira
                numero_formatado = self.formatar_numero(numero)
                resultado_formatado = self.formatar_numero(resultado)
                calculo_str = f"√{numero_formatado} = {resultado_formatado}"
                self.historico.append(calculo_str)
                self.atualizar_lista_historico()

                # Mostrar resultado formatado
                resultado_str = self.formatar_numero(resultado)
                self.resultado_var.set(resultado_str)
                self.expressao = str(resultado)
                self.expressao_calculada = str(resultado)
        except:
            messagebox.showerror("Erro", "Erro ao calcular raiz quadrada!")

    def trocar_sinal(self):
        try:
            if self.expressao_calculada and self.expressao_calculada != "0":
                if self.expressao_calculada.startswith('-'):
                    self.expressao_calculada = self.expressao_calculada[1:]
                    self.expressao = self.expressao[1:]
                else:
                    self.expressao_calculada = '-' + self.expressao_calculada
                    self.expressao = '-' + self.expressao
                self.atualizar_display()
        except:
            pass

    def desformatar_numero(self, numero_str):
        """Remove formatação brasileira e converte para número"""
        try:
            # Remove pontos (separadores de milhares) e troca vírgula por ponto
            numero_limpo = numero_str.replace('.', '').replace(',', '.')
            return float(numero_limpo)
        except:
            return numero_str

    def atualizar_lista_historico(self):
        """Atualiza a lista do histórico na interface"""
        self.lista_historico.delete(0, tk.END)
        for item in self.historico:
            self.lista_historico.insert(tk.END, item)
        # Fazer scroll para o final (último item)
        self.lista_historico.see(tk.END)

    def limpar_historico(self):
        """Limpa todo o histórico"""
        self.historico.clear()
        self.lista_historico.delete(0, tk.END)

    def toggle_historico(self):
        """Mostra ou oculta o painel do histórico"""
        if self.historico_visivel:
            # Ocultar histórico
            self.frame_historico.pack_forget()
            self.root.geometry("400x600")
            self.btn_historico.config(text="Mostrar Histórico")
            self.historico_visivel = False
        else:
            # Mostrar histórico
            self.frame_historico.pack(side='right', fill='both', expand=False, padx=(10, 0))
            self.root.geometry("650x600")
            self.btn_historico.config(text="Ocultar Histórico")
            self.historico_visivel = True

    def executar(self):
        self.root.mainloop()


# Para executar a calculadora
if __name__ == "__main__":
    calc = Calculadora()
    calc.executar()