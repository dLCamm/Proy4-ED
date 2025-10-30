import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from funciones.claves import llaves

ventana = tk.Tk()
ventana.title("Cifrado y Firma Digital")
ventana.geometry("600x600")

#Las ventanas de cada funcion
notebook = ttk.Notebook(ventana)
notebook.pack(fill='both', expand=True)

nbclave = tk.Frame(notebook)
nbcifrado = tk.Frame(notebook)
nbfirma = tk.Frame(notebook)

notebook.add(nbclave, text="Generar Claves")
notebook.add(nbcifrado, text="Cifrar/Descifrar")
notebook.add(nbfirma, text="Firmar/Verificar")

# Generar Llave publica y privada
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

#Generar firma digital y verificar firma 
etiqueta_firma = tk.Label(nbfirma, text="Mensaje a Firmar:", font=("Arial", 12))
etiqueta_firma.pack(pady=5)

texto_a_firmar = tk.Text(nbfirma, height=3, width=50)
texto_a_firmar.pack(pady=5)

etiqueta_resultado_firma = tk.Label(nbfirma, text="", fg="blue")
etiqueta_resultado_firma.pack(pady=5)

etiqueta_firma_gen = tk.Label(nbfirma, text="Firma Generada (Base64):", font=("Arial", 10))
etiqueta_firma_gen.pack(pady=5)

texto_firma_gen = tk.Text(nbfirma, height=3, width=50, wrap='word', bd=1, relief="solid")
texto_firma_gen.pack(pady=5)

#Función para poder firmar digitalmente
def firmar():
    """Función para firmar el texto ingresado."""
    mensaje = texto_a_firmar.get("1.0", tk.END).strip()
    if not mensaje:
        messagebox.showerror("Error", "El campo de mensaje a firmar está vacío.")
        return

    mensaje_bytes = mensaje.encode('utf-8')
    
    firma_bytes = llaves.firmar_mensaje(mensaje_bytes)
    
    if firma_bytes:
        import base64
        firma_base64 = base64.b64encode(firma_bytes).decode('utf-8')
        texto_firma_gen.delete("1.0", tk.END)
        texto_firma_gen.insert("1.0", firma_base64)

        messagebox.showinfo("Firma", "Mensaje firmado correctamente. La firma aparece en el campo de arriba y puede ser copiada.")
        etiqueta_resultado_firma.config(text=f"Firma Generada (Base64):\n{firma_base64}", fg="green")
        
        global ultima_firma
        global ultimo_mensaje
        ultima_firma = firma_bytes
        ultimo_mensaje = mensaje_bytes
        messagebox.showinfo("Firma", "Mensaje firmado correctamente.")

btn_firmar = tk.Button(nbfirma, text="Firmar Mensaje", command=firmar)
btn_firmar.pack(pady=10)

ultima_firma = None
ultimo_mensaje = None

etiqueta_verificacion = tk.Label(nbfirma, text="--- Verificación ---", font=("Arial", 12))
etiqueta_verificacion.pack(pady=10)

etiqueta_verif_firma = tk.Label(nbfirma, text="Firma Digital (Base64):", font=("Arial", 10))
etiqueta_verif_firma.pack(pady=5)

texto_firma_verif = tk.Text(nbfirma, height=3, width=50)
texto_firma_verif.pack(pady=5)

etiqueta_aviso_verificacion = tk.Label(nbfirma, text="Asegúrese de que el Mensaje en el campo de arriba\nsea el que desea verificar con la Firma.", fg="red")
etiqueta_aviso_verificacion.pack(pady=5)

etiqueta_resultado_verificacion = tk.Label(nbfirma, text="Resultado: Pendiente", font=("Arial", 12, "bold"), fg="black")
etiqueta_resultado_verificacion.pack(pady=5)

#Función para poder verificar la firma 
def verificar():
    """Función para verificar la firma."""
    mensaje_a_verificar = texto_a_firmar.get("1.0", tk.END).strip()
    if not mensaje_a_verificar:
        messagebox.showerror("Error", "El campo de mensaje a verificar está vacío.")
        return
    
    firma_base64 = texto_firma_verif.get("1.0", tk.END).strip()
    if not firma_base64:
        messagebox.showerror("Error", "El campo de firma a verificar está vacío.")
        return
    
    try:
        import base64
        firma_bytes = base64.b64decode(firma_base64)

        mensaje_bytes = mensaje_a_verificar.encode('utf-8')

        es_valida = llaves.verificar_firma(mensaje_bytes, firma_bytes)
        
        if es_valida:
            etiqueta_resultado_verificacion.config(text="Resultado: ¡FIRMA VÁLIDA! (Integridad y autenticidad OK)", fg="green")
        else:
            etiqueta_resultado_verificacion.config(text="Resultado: ¡FIRMA INVÁLIDA! (El mensaje fue alterado o la firma es incorrecta)", fg="red")

    except Exception as e:
        messagebox.showerror("Error", f"Error de decodificación o verificación. Asegúrese de que el texto de la firma sea Base64 válido. Error: {e}")

btn_verificar = tk.Button(nbfirma, text="Verificar Firma", command=verificar)
btn_verificar.pack(pady=10)














ventana.mainloop()