from textblob import TextBlob
from googletrans import Translator
import re
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
#from datos.datos import obtener_datos_etiquetados  # Asegúrate de que esta función esté presente



def validar_texto(texto):
    """Función que valida el texto ingresado."""
    if not texto or texto == "Ingrese texto aquí...":
      return False
    if not re.match(r"^[a-zA-Z\s.,@áóíúéñüÉÁÚÍÓ1234567890;:?¿!¡\\n]*$", texto):  # Solo letras y espacios
       return False
    return True

class SentimentLogic:
    translator = Translator()
    
    @staticmethod
    def analizar_sentimiento(texto):
        if not validar_texto(texto):  # Llamada a la función de validación
            print("Texto no válido. Asegúrate de ingresar un texto correcto.")
            return "Neutro"
        try:
            # Traducir el texto a inglés
            texto_traducido = SentimentLogic.translator.translate(texto, dest='en').text
            print(f"Texto traducido: '{texto_traducido}'")

            if not texto_traducido:
                print("La traducción devolvió un string vacío.")
                return "Neutro"
            blob = TextBlob(texto_traducido)
            sentimiento = blob.sentiment.polarity           
            # Inicializar el resultado como neutro
            resultado = "neutro"
            # Definición de palabras clave
            palabras_clave_negativas = ["repetitivo", "aburrido", "malo", "suenan igual", "pobre", "demasiado largo", "no me gusta","te extraño"]
            palabras_clave_positivas = ["genial", "me encanta", "excelente", "fantástico", "bueno", "maravilloso", "Admiro","gratificante, asombroso,espectacular"]
            # Verificación con palabras clave
            if any(palabra in texto.lower() for palabra in palabras_clave_negativas):
                resultado = "Negativo"
            elif any(palabra in texto.lower() for palabra in palabras_clave_positivas):
                resultado = "Positivo"
            elif sentimiento > 0.1:
                resultado = "Positivo"
            elif sentimiento < -0.1:
                resultado = "Negativo"
            else:
                resultado= "Neutro"
            print(f"Texto: '{texto}' | Sentimiento: {sentimiento} | Resultado: {resultado}")
            return resultado
        except Exception as e:
            print(f"Error en la traducción: {e}")
            return "Neutro"

def predecir_sentimientos(textos):
    predicciones = []
    for texto in textos:
        resultado = SentimentLogic.analizar_sentimiento(texto)
        predicciones.append(resultado)
    return predicciones

def evaluar_modelo(datos_etiquetados, predicciones):
    etiquetas_reales = [dato[1] for dato in datos_etiquetados]
    accuracy = accuracy_score(etiquetas_reales, predicciones)
    precision = precision_score(etiquetas_reales, predicciones, average='weighted', zero_division=0)
    recall = recall_score(etiquetas_reales, predicciones, average='weighted', zero_division=0)
    f1 = f1_score(etiquetas_reales, predicciones, average='weighted', zero_division=0)
#print("datos reales" ,etiquetas_reales)

    return accuracy, precision, recall, f1

# Nueva función para ejecutar el proceso de evaluación
""" def evaluar_y_mostrar_resultados():
    datos_etiquetados = obtener_datos_etiquetados()
    textos = [dato[0] for dato in datos_etiquetados]

    # Predicción de sentimientos
    predicciones = predecir_sentimientos(textos)

    # Evaluación
    accuracy, precision, recall, f1 = evaluar_modelo(datos_etiquetados, predicciones)

    # Imprimir resultados
    print(f"Exactitud: {accuracy:.2f}")
    print(f"Precisión: {precision:.2f}")
    print(f"Exhaustividad (Recall): {recall:.2f}")
    print(f"F1 Score: {f1:.2f}") """
