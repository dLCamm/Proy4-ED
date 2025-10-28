from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from tkinter import messagebox
import os

class claves:
    def __init__(self):
        self.keyprivada = None
        self.keypublica = None

    def generar_claves(self):
        self.keyprivada = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        self.keypublica = self.keyprivada.public_key()
   

    # Aca se guardan las key en archivos .pem
    def guardar_claves(self, private_path="keyprivada.pem", public_path="keypublica.pem"):
        # Para la clave privada
        self.generar_claves()
        with open(f"llaves/{private_path}", "wb") as f:
            f.write(
                self.keyprivada.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()  # sin contraseña
                )
            )

        # Para la clave pública
        with open(f"llaves/{public_path}", "wb") as f:
            f.write(
                self.keypublica.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
            )

        messagebox.showinfo("Claves", "Las claves se han guardado correctamente en la carpeta llaves")

    # Esta es para cargar las claves desde archivos
    def cargar_claves(self, private_path="llaves/keyprivada.pem", public_path="llaves/keypublica.pem"):

        if not os.path.exists(private_path) or not os.path.exists(public_path):
            messagebox.showerror("Error", "Primero debe generar las llaves")
            return

        with open(private_path, "rb") as f:
            self.keyprivada = serialization.load_pem_private_key(f.read(), password=None)


        with open(public_path, "rb") as f:
            self.keypublica = serialization.load_pem_public_key(f.read())
        messagebox.showinfo("Claves", "Las claves se han cargado correctamente")

llaves = claves()