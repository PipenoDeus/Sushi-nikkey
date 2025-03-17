import sqlite3


def conectar():
    return sqlite3.connect("sushi_nikkey.db")


def crear_tabla():
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            rut TEXT PRIMARY KEY,
            nombre TEXT NOT NULL,
            direccion TEXT,
            comuna TEXT,
            correo TEXT UNIQUE,
            edad INTEGER,
            celular TEXT,
            tipo TEXT
        )
    """)
    conn.commit()
    conn.close()


def insertar_cliente(rut, nombre, direccion, comuna, correo, edad, celular, tipo):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO clientes (rut, nombre, direccion, comuna, correo, edad, celular, tipo) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                       (rut, nombre, direccion, comuna, correo, int(edad), celular, tipo))
        conn.commit()
        return True  # Éxito
    except sqlite3.IntegrityError:
        return False  # Error (RUT duplicado)
    finally:
        conn.close()


def obtener_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return clientes


crear_tablas()
