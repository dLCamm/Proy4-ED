import tkinter as tk
from tkinter import ttk
from funciones.claves import llaves

ventana = tk.Tk()
ventana.title("Cifrado y Firma Digital")
ventana.geometry("500x300")

#Las ventanas de cada funcion
notebook = ttk.Notebook(ventana)
notebook.pack(fill='both', expand=True)

nbclave = tk.Frame(notebook)
nbcifrado = tk.Frame(notebook)
nbfirma = tk.Frame(notebook)

notebook.add(nbclave, text="Generar Claves")
notebook.add(nbcifrado, text="Cifrar/Descifrar")
notebook.add(nbfirma, text="Firmar/Verificar")

saludo = tk.Label(nbclave, text="Generar Llave publica y Privada", font=("Arial", 16))
saludo.pack(pady=10)

def crearllaves():
    llaves.guardar_claves()
    llavessi.config(text="Las llaves fueron actualizadas, porfavor cargarlas")

button_generar = tk.Button(nbclave, text="Crear Llaves", font=("Arial", 14), width=20, command=lambda: crearllaves())
button_generar.pack(pady=20)

def carga():
    llaves.cargar_claves()
    if llaves.keyprivada and llaves.keypublica:
        llavessi.config(text="Las llaves estan cargadas")
        print(llaves.keyprivada, llaves.keypublica)

button_cargar = tk.Button(nbclave, text="Cargar Llaves", font=("Arial", 14), width=20, command=lambda: carga())
button_cargar.pack(pady=20)

llavessi = tk.Label(nbclave, text="Las llaves aún no han sido cargadas", font=("Arial", 12))
llavessi.pack(pady=10)














ventana.mainloop()