import sqlite3

def crear_base_datos():
    conn = sqlite3.connect('sentimientos.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resultados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            texto TEXT NOT NULL,
            sentimiento TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

def insertar_resultado(texto, sentimiento):
    conn = sqlite3.connect('sentimientos.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT sentimiento FROM resultados WHERE texto = ?", (texto,))
        resultado = cursor.fetchone()

        if resultado is None:
            cursor.execute('''
                INSERT INTO resultados (texto, sentimiento)
                VALUES (?, ?);
            ''', (texto, sentimiento))
            conn.commit()
            print("Comentario insertado correctamente.")
            return sentimiento  # Retorna el nuevo sentimiento
        
        else:
            print("El comentario ya existe en la base de datos.")
            return resultado[0]  # Retorna el sentimiento existente
    finally:
        conn.close()  # Esto asegura que siempre se cierre la conexión

def obtener_datos_etiquetados():
    conn = sqlite3.connect('sentimientos.db')  # Cambia por tu archivo de base de datos
    cursor = conn.cursor()
    cursor.execute("SELECT texto, sentimiento FROM resultados")  # Ajusta para que coincida con tu tabla
    datos = cursor.fetchall()
#print("Datos etiquetados:",datos)

    conn.close()
    return datos

crear_base_datos()
