import tkinter as tk
from tkinter import ttk
import itertools
import math

# Função para validar se os campos de entrada estão preenchidos antes de habilitar o botão de cálculo
def validate_entries():
    if not ratio_entry.get() or not range_start_entry.get() or not range_end_entry.get() or not combinations_entry.get():
        calculate_button.config(state='disabled')
    else:
        calculate_button.config(state='normal')

# Função para validar se os campos de entrada da constante estão preenchidos antes de habilitar o botão de cálculo da constante
def validate_constant_entries():
    if not helix_angle_entry.get() or not module_entry.get():
        calculate_constant_button.config(state='disabled')
    else:
        calculate_constant_button.config(state='normal')

# Função para calcular as combinações de engrenagens que atendem à relação desejada
def calculate():
    try:
        # Obtém os valores dos campos de entrada
        desired_ratio = float(ratio_entry.get().replace(',', '.'))
        unavailable_gears = list(map(int, gears_entry.get().split(","))) if gears_entry.get() else []
        gear_range_start = int(range_start_entry.get())
        gear_range_end = int(range_end_entry.get())
        combinations_number = int(combinations_entry.get())

        # Cria um intervalo de engrenagens disponíveis, excluindo as indisponíveis
        gear_range = list(range(gear_range_start, gear_range_end+1))
        for gear in unavailable_gears:
            if gear in gear_range:
                gear_range.remove(gear)

        count = 0

        # Itera sobre todas as combinações possíveis e verifica se a relação é a desejada
        for combination in itertools.product(gear_range, repeat=4):
            A, B, C, D = combination
            ratio = (A * C) / (B * D)
            if abs(ratio - desired_ratio) < 1e-5:
                result_text.config(state='normal')  # ativar o widget
                result_text.insert(tk.END, f"A={A}, B={B}, C={C}, D={D}  relação {ratio}\n")  # inserir o texto
                result_text.config(state='disabled')  # desativar o widget
                count += 1
            if count == combinations_number:
                break
        # Exibe mensagem se nenhuma combinação for encontrada
        if count == 0:
            result_text.config(state='normal')  # ativar o widget
            result_text.insert(tk.END, "Nenhuma combinação de engrenagens encontrada para a relação desejada.\n")  # inserir o texto
            result_text.config(state='disabled')  # desativar o widget
    except Exception as e:
        result_text.config(state='normal')  # ativar o widget
        result_text.insert(tk.END, f"Erro: {str(e)}\n")  # inserir o texto
        result_text.config(state='disabled')  # desativar o widget


# Função para calcular a relação com base na constante, ângulo de hélice e módulo
def calculate_constant():
    constant = float(constant_combobox.get())
    helix_angle_deg = float(helix_angle_entry.get().replace(',', '.'))
    helix_angle_rad = math.radians(helix_angle_deg)  # Convertendo de graus para radianos
    module = float(module_entry.get().replace(',', '.'))
    ratio = abs(constant * (math.sin(helix_angle_rad) / module))  # Passando o valor em radianos para a função sin()
    ratio_entry.delete(0, tk.END)
    ratio_entry.insert(0, ratio)


# Função para limpar todos os campos de entrada e o campo de texto de resultado
def clear_all():
    ratio_entry.delete(0, tk.END)
    gears_entry.delete(0, tk.END)
    range_start_entry.delete(0, tk.END)
    range_end_entry.delete(0, tk.END)
    combinations_entry.delete(0, tk.END)
    helix_angle_entry.delete(0, tk.END)
    module_entry.delete(0, tk.END)
    result_text.config(state='normal')  # habilitar o widget
    result_text.delete(1.0, tk.END)  # limpar o campo de texto
    result_text.config(state='disabled')  # desabilitar o widget novamente

# Configurações iniciais da interface gráfica Tkinter
root = tk.Tk()
root.title("Cálculadora para relação de engrenagens")
root.geometry('400x650') 
root.resizable(False, False)
root.iconbitmap('favicon.ico')

# Criação e configuração dos frames e widgets da interface gráfica
main_frame = tk.Frame(root)
main_frame.pack(padx=10)

# Primeiro cálculo
frame1 = tk.Frame(main_frame, borderwidth=2, relief='groove')  
frame1.pack(padx=10, pady=10,  fill='both', expand=True)  

frame1_title = tk.Label(frame1, text="Cálculo da relação", font=("Helvetica", 14))  
frame1_title.pack(anchor='w')


constant_label = tk.Label(frame1, text="Insira a constante da máquina:", font=("Helvetica", 10))
constant_label.pack(anchor='w')

constant_combobox = ttk.Combobox(frame1, values=[2.541666, 9], font=("Helvetica", 12))
constant_combobox.pack(anchor='w')

helix_angle_label = tk.Label(frame1, text="Insira o ângulo de hélice (decimal):", font=("Helvetica", 10))
helix_angle_label.pack(anchor='w')

helix_angle_entry = tk.Entry(frame1, font=("Helvetica"))
helix_angle_entry.pack(anchor='w')

module_label = tk.Label(frame1, text="Insira o módulo:", font=("Helvetica", 10))
module_label.pack(anchor='w')

module_entry = tk.Entry(frame1, font=("Helvetica"))
module_entry.pack(anchor='w')

calculate_constant_button = tk.Button(frame1, text="Calcular relação", command=calculate_constant, state='disabled', font=("Helvetica", 10))
calculate_constant_button.pack(anchor='w')

# Segundo cálculo
frame2 = tk.Frame(main_frame, borderwidth=2, relief='groove')  
frame2.pack(padx=10, pady=10)  
frame2_title = tk.Label(frame2, text="Cálculo de engrenagens", font=("Helvetica", 14))  
frame2_title.pack(anchor='w')

ratio_label = tk.Label(frame2, text="Insira a relação desejada:", font=("Helvetica", 10))
ratio_label.pack(anchor='w')

ratio_entry = tk.Entry(frame2, font=("Helvetica", 12))
ratio_entry.pack(anchor='w')

gears_label = tk.Label(frame2, text="Insira as engrenagens indisponíveis (separadas por vírgulas):", font=("Helvetica", 10))
gears_label.pack(anchor='w')

gears_entry = tk.Entry(frame2, font=("Helvetica"))
gears_entry.pack(anchor='w')

range_start_label = tk.Label(frame2, text="Insira o início do intervalo de engrenagens:", font=("Helvetica", 10))
range_start_label.pack(anchor='w')

range_start_entry = tk.Entry(frame2, font=("Helvetica"))
range_start_entry.pack(anchor='w')

range_end_label = tk.Label(frame2, text="Insira o fim do intervalo de engrenagens:", font=("Helvetica", 10))
range_end_label.pack(anchor='w')

range_end_entry = tk.Entry(frame2, font=("Helvetica"))
range_end_entry.pack(anchor='w')

combinations_label = tk.Label(frame2, text="Insira o número de combinações desejadas:", font=("Helvetica", 10))
combinations_label.pack(anchor='w')

combinations_entry = tk.Entry(frame2, font=("Helvetica"))
combinations_entry.pack(anchor='w')

calculate_button = tk.Button(frame2, text="Calcular engrenagens", command=calculate, state='disabled', font=("Helvetica", 10))
calculate_button.pack(anchor='w')

clear_button = tk.Button(frame2, text="Limpar", command=clear_all, font=("Helvetica", 10))
clear_button.pack(anchor='w')

result_text = tk.Text(frame2, state='disabled', font=("Helvetica", 10))
result_text.pack(anchor='w')

# Vincula os campos de entrada às funções de validação para habilitar/desabilitar os botões de cálculo

entries = [ratio_entry, gears_entry, range_start_entry, range_end_entry, combinations_entry]
constant_entries = [helix_angle_entry, module_entry]

for entry in entries:
    entry.bind("<KeyRelease>", lambda event: validate_entries())

for entry in constant_entries:
    entry.bind("<KeyRelease>", lambda event: validate_constant_entries())

root.mainloop()
