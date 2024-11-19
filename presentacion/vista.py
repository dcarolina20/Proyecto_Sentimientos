import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from logica.negocio import SentimentLogic, validar_texto
from datos.datos import insertar_resultado




# Cargar la interfaz gráfica
class SentimentAppGUI:
    def __init__(self, ventana):
        self.ventana = ventana
        self.configurar_ventana()
        self.cargar_elementos_gui()

    def configurar_ventana(self):
        self.ventana.title("Análisis de Sentimientos")
        self.ventana.geometry("600x300")
        self.ventana.config(bg="#413e3e")
        self.ventana.resizable(False, False)
        self.centrar_ventana(self.ventana)

    def cargar_elementos_gui(self):
        
        imagen_fondo = Image.open("C:/Users/Carolina/OneDrive - Universidad de Pamplona/10 semestre/Analisis de sentimientos/images/fondo.jpg")
        imagen_fondo = imagen_fondo.resize((200, 250), Image.LANCZOS)  # Asegúrate de que la imagen tenga el tamaño adecuado
        imagen_fondo_tk = ImageTk.PhotoImage(imagen_fondo)
        
        canvas = tk.Canvas(self.ventana, width=200, height=250, bg="#413e3e", highlightthickness=0)  # Desactivar el borde de enfoque
        canvas.place(relx=1, y=50, anchor='ne')  # Cambia la ubicación aquí

        # Añadir la imagen de fondo en el canvas
        canvas.create_image(0, 0, anchor="nw", image=imagen_fondo_tk)

        # Encabezado principal
        self.encabezado_principal = tk.Frame(self.ventana, bg="black", width=600, height=50)
        self.encabezado_principal.pack(side=tk.TOP, fill=tk.X)

        # Frame interno para agrupar logo y texto en la misma línea
        frame_interno = tk.Frame(self.encabezado_principal, bg="black")
        frame_interno.pack(side=tk.LEFT, padx=10)
        
           # Cargar y redimensionar el logo de Twitter
        ruta_logo = "C:/Users/Carolina/OneDrive - Universidad de Pamplona/10 semestre/Analisis de sentimientos/images/twitter_logo.png"
        imagen_original = Image.open(ruta_logo)
        imagen_redimensionada = imagen_original.resize((50, 50), Image.LANCZOS)
        self.logo_twitter = ImageTk.PhotoImage(imagen_redimensionada)
        

        # Colocar el logo en el encabezado (a la izquierda del texto)
        etiqueta_logo = tk.Label(frame_interno, image=self.logo_twitter, bg="black")
        etiqueta_logo.pack(side=tk.LEFT, padx=10, pady=5)
        
       
        # Título en el encabezado (a la derecha del logo, centrado verticalmente)
        titulo_principal = tk.Label(frame_interno, text="ANÁLISIS DE \nSENTIMIENTOS", font=("Helvetica", 14,"bold"), bg="black", fg="white" )
        titulo_principal.pack(side=tk.LEFT, padx=10 )
        
       

        # Frame izquierdo para estrellas y caritas
        frame_izquierda = tk.Frame(self.ventana, bg="#413e3e")
        frame_izquierda.pack(side=tk.LEFT, padx=10)

        # Añadir estrellitas
        estrellitas_label = tk.Label(frame_izquierda, text="⭐ ⭐ ⭐ ⭐ ⭐", font=("Arial", 12), bg="#413e3e", fg="white")
        estrellitas_label.pack(side=tk.TOP, pady=(10, 5))

        # Frame para las caritas y los nombres
        frame_caritas = tk.Frame(frame_izquierda, bg="#413e3e")
        frame_caritas.pack(side=tk.TOP)

        # Positivo
        frame_positivo = tk.Frame(frame_caritas, bg="#413e3e")
        frame_positivo.pack(side=tk.TOP, pady=5, anchor='w')

        carita_positiva = tk.Label(frame_positivo, text="😊", font=("Arial", 20), bg="#413e3e", fg="white")
        carita_positiva.pack(side=tk.LEFT)

        etiqueta_positiva = tk.Label(frame_positivo, text="Positivo", font=("Arial", 12), bg="#413e3e", fg="white")
        etiqueta_positiva.pack(side=tk.LEFT, padx=(5, 0))

        # Neutro
        frame_neutro = tk.Frame(frame_caritas, bg="#413e3e")
        frame_neutro.pack(side=tk.TOP, pady=5, anchor='w')

        carita_neutra = tk.Label(frame_neutro, text="😐", font=("Arial", 20), bg="#413e3e", fg="white")
        carita_neutra.pack(side=tk.LEFT)

        etiqueta_neutra = tk.Label(frame_neutro, text="Neutro", font=("Arial", 12), bg="#413e3e", fg="white")
        etiqueta_neutra.pack(side=tk.LEFT, padx=(5, 0))

        # Negativo
        frame_negativo = tk.Frame(frame_caritas, bg="#413e3e")
        frame_negativo.pack(side=tk.TOP, pady=5, anchor='w')

        carita_negativa = tk.Label(frame_negativo, text="😞", font=("Arial", 20), bg="#413e3e", fg="white")
        carita_negativa.pack(side=tk.LEFT)

        etiqueta_negativa = tk.Label(frame_negativo, text="Negativo", font=("Arial", 12), bg="#413e3e", fg="white")
        etiqueta_negativa.pack(side=tk.LEFT, padx=(5, 0))

        # Línea vertical antes de la caja de texto
        linea_vertical = tk.Canvas(self.ventana, width=1, height=250, bg='white')
        linea_vertical.pack(side=tk.LEFT, anchor="nw", padx=(0, 10), pady=(10, 10))
        
        frame_derecha = tk.Frame(self.ventana, bg="#413e3e")
        frame_derecha.pack(side=tk.LEFT, padx=20, pady=10)

        # Campo de texto en la parte derecha (ajusta width a un valor mayor)
        self.entrada_texto = tk.Text(frame_derecha, font=("Arial", 12), width=30, height=2 , bg="#202327", fg="white", bd=0)  # Cambia width a 30 
        self.entrada_texto.insert("1.0", "Ingrese texto aquí...")
        self.entrada_texto.pack(padx=13, pady=10)
                
      
        boton_generar = tk.Button(frame_derecha, text="Generar", font=("Arial", 12), command=self.analizar_sentimiento, bg="#1e90ff", fg="white")
        boton_generar.pack(pady=10)

        # Bind para manejar el placeholder
        self.entrada_texto.bind("<FocusIn>", self.on_entry_click)
        self.entrada_texto.bind("<FocusOut>", self.on_focusout)

    def centrar_ventana(self, ventana):
        self.ventana.update_idletasks()
        ancho_ventana = self.ventana.winfo_width()
        alto_ventana = self.ventana.winfo_height()
        ancho_pantalla = self.ventana.winfo_screenwidth()
        alto_pantalla = self.ventana.winfo_screenheight()
        x = (ancho_pantalla // 2) - (ancho_ventana // 2)
        y = (alto_pantalla // 2) - (alto_ventana // 2)
        ventana.geometry(f"{ancho_ventana}x{alto_ventana}+{x}+{y}")

    def on_entry_click(self, event):
        if self.entrada_texto.get("1.0", "end-1c").strip() == "Ingrese texto aquí...":
            self.entrada_texto.delete("1.0", "end")
            self.entrada_texto.config(fg="#FFFFFF")

    def on_focusout(self, event):
        if self.entrada_texto.get("1.0", "end-1c").strip() == "":
            self.entrada_texto.insert("1.0", "Ingrese texto aquí...")
            self.entrada_texto.config(fg="#A9A9A9")
            
    def analizar_sentimiento(self):
        texto = self.entrada_texto.get("1.0", tk.END).strip()
        if validar_texto(texto):
            resultado_texto = SentimentLogic.analizar_sentimiento(texto)
            insertar_resultado(texto, resultado_texto)
            self.mostrar_resultados_1(resultado_texto)
        else:
            messagebox.showerror("Error", "Por favor, ingresa un texto válido.")


    
    def mostrar_resultados_1(self, resultado_texto):
        ventana_resultados = tk.Toplevel(self.ventana)
        ventana_resultados.title("Resultados del Análisis")
        ventana_resultados.geometry("600x300")
        ventana_resultados.config(bg="#413e3e")
        ventana_resultados.resizable(False,False)
        self.ventana.withdraw()
        
        
        self.centrar_ventana(ventana_resultados)

        imagen_fondo2 = Image.open("C:/Users/Carolina/OneDrive - Universidad de Pamplona/10 semestre/Analisis de sentimientos/images/fondo2.jpg")
        imagen_fondo2 = imagen_fondo2.resize((200, 250), Image.LANCZOS)  # Asegúrate de que la imagen tenga el tamaño adecuado
        imagen2_fondo_tk = ImageTk.PhotoImage(imagen_fondo2)

        canvas2 = tk.Canvas(ventana_resultados, width=200, height=250, bg="#413e3e", highlightthickness=0)  # Remove focus border
        canvas2.place(relx=0.0001, rely=1, anchor='sw')  # Adjust the placement using relx, rely

        canvas2.image = imagen2_fondo_tk
        canvas2.create_image(0, 0, anchor="nw", image=imagen2_fondo_tk)


        # Añadir la imagen de fondo en el canvas

        imagen_fondo3 = Image.open("C:/Users/Carolina/OneDrive - Universidad de Pamplona/10 semestre/Analisis de sentimientos/images/fondo.jpg")
        imagen_fondo3 = imagen_fondo3.resize((200, 250), Image.LANCZOS)  # Asegúrate de que la imagen tenga el tamaño adecuado
        imagen3_fondo_tk = ImageTk.PhotoImage(imagen_fondo3)

        canvas3 = tk.Canvas(ventana_resultados, width=200, height=250, bg="#413e3e", highlightthickness=0)  # Desactivar el borde de enfoque
        canvas3.place(relx=1, y=50, anchor='ne')  # Cambia la ubicación aquí

        canvas3.image = imagen3_fondo_tk

        canvas3.create_image(0, 0, anchor="nw", image=imagen3_fondo_tk)

        encabezado_resultados = tk.Frame(ventana_resultados, bg="black", width=600, height=50)
        encabezado_resultados.pack(side=tk.TOP, fill=tk.X)

        # Marco interno para el logo y el título
        frame_interno2 = tk.Frame(encabezado_resultados, bg="black")
        frame_interno2.pack(side=tk.LEFT, padx=10, pady=5)
        
        # Etiqueta del logo en el marco interno
        
        # Colocar el logo en el encabezado (a la izquierda del texto)
        etiqueta_logo = tk.Label(frame_interno2, image=self.logo_twitter, bg="black")
        etiqueta_logo.pack(side=tk.LEFT, padx=10)

        # Título en el mismo marco interno
        titulo_resultados = tk.Label(frame_interno2, text="ANÁLISIS DE \nSENTIMIENTOS", font=("Arial", 14, "bold"), bg="black", fg="white")
        titulo_resultados.pack(side=tk.LEFT, padx=3, pady=10) 

        # Crear un nuevo frame para el subtítulo dentro del encabezado
        frame_subtitulo = tk.Frame(encabezado_resultados, bg="black")
        frame_subtitulo.pack(side=tk.RIGHT, padx=10, pady=5)

        # Subtítulo en su propio marco
        subtitulo_resultados = tk.Label(frame_subtitulo, text="RESULTADOS", font=("Arial", 12, "bold"), bg="black", fg="white")
        subtitulo_resultados.pack(padx=10, pady=4)


        if resultado_texto == "Positivo":
            imagen_medidor = "C:/Users/Carolina/OneDrive - Universidad de Pamplona/10 semestre/Analisis de sentimientos/images/positivo.png"
            carita = "😊"
        elif resultado_texto == "Neutro":
            imagen_medidor = "C:/Users/Carolina/OneDrive - Universidad de Pamplona/10 semestre/Analisis de sentimientos/images/neutro.png"
            carita = "😐"
        else:
            imagen_medidor = "C:/Users/Carolina/OneDrive - Universidad de Pamplona/10 semestre/Analisis de sentimientos/images/negativo.png"
            carita = "😞"

        imagen_medidor_cargada = Image.open(imagen_medidor)
        imagen_medidor_cargada = imagen_medidor_cargada.resize((100, 100), Image.LANCZOS)
        imagen_medidor_tk = ImageTk.PhotoImage(imagen_medidor_cargada)

        etiqueta_medidor = tk.Label(ventana_resultados, image=imagen_medidor_tk, bg="#413e3e")
        etiqueta_medidor.image = imagen_medidor_tk  # Mantener una referencia para evitar que sea recolectada
        etiqueta_medidor.pack(pady=10)

        # Mostrar la carita (emoji) y el resultado textual
        etiqueta_resultado = tk.Label(ventana_resultados, text=f"{carita}  {resultado_texto}", font=("Arial", 17, "bold"), bg="#413e3e", fg="black")
        etiqueta_resultado.pack(pady=5)
            

        boton_cerrar = tk.Button(ventana_resultados, text="Regresar", font=("Arial", 12), command=lambda: self.regresar_a_principal(ventana_resultados), bg="#1e90ff", fg="white")
        boton_cerrar.pack(pady=6)
       

    def regresar_a_principal(self, ventana_resultados):
        self.entrada_texto.delete("1.0", tk.END)
        self.entrada_texto.insert("1.0", "Ingrese texto aquí...")
        self.entrada_texto.config(fg="#A9A9A9")
        ventana_resultados.destroy()
        self.ventana.deiconify()
        self.centrar_ventana(self.ventana)
        
        

    
if __name__ == "__main__":
    root = tk.Tk()
    app = SentimentAppGUI(root) 
    root.mainloop()
   # evaluar_y_mostrar_resultados()