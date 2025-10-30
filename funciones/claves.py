from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature
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


    def firmar_mensaje(self, mensaje: bytes) -> bytes:
        if self.keyprivada is None:
            messagebox.showerror("Error", "Debe cargar o generar las claves primero.")
            return b""
        
        try:
            firma = self.keyprivada.sign(
                mensaje,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return firma
        except Exception as e:
            messagebox.showerror("Error", f"Error al firmar: {e}")
            return b""


    def verificar_firma(self, mensaje: bytes, firma: bytes) -> bool:
        if self.keypublica is None:
            messagebox.showerror("Error", "Debe cargar o generar las claves primero.")
            return False

        try:
            self.keypublica.verify(
                firma,
                mensaje,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True 
        except InvalidSignature:
            return False 
        except Exception as e:
            messagebox.showerror("Error", f"Error de verificación: {e}")
            return False

llaves = claves()