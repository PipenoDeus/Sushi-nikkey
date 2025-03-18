import tkinter as tk
import sqlite3
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk


def registrar_admin(usuario, contrasena):
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO administradores (usuario, contrasena) VALUES (?, ?)", (usuario, contrasena))
        conn.commit()
        print("Administrador registrado con éxito.")
    except sqlite3.IntegrityError:
        print("Error: El usuario ya existe.")
    
    conn.close()

def login_admin():
    login_window = tk.Toplevel(root)  # Crear ventana de login
    login_window.title("Login Administrador")

    # Campos de usuario y contraseña
    tk.Label(login_window, text="Usuario:").grid(row=0, column=0)
    entry_usuario = tk.Entry(login_window)
    entry_usuario.grid(row=0, column=1)

    tk.Label(login_window, text="Contraseña:").grid(row=1, column=0)
    entry_contrasena = tk.Entry(login_window, show="*")  # Ocultar contraseña
    entry_contrasena.grid(row=1, column=1)

    def verificar_login():
        usuario = entry_usuario.get()
        contrasena = entry_contrasena.get()

        conn = sqlite3.connect("clientes.db")
        cursor = conn.cursor()

        # Buscar en la base de datos
        cursor.execute("SELECT * FROM administradores WHERE usuario = ? AND contrasena = ?", (usuario, contrasena))
        admin = cursor.fetchone()
        conn.close()

        if admin:
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
            login_window.destroy()
            habilitar_botones()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    # Botón para iniciar sesión
    tk.Button(login_window, text="Iniciar Sesión", command=verificar_login).grid(row=2, columnspan=2)

def registrar_cliente():
    def guardar_cliente():
        rut = entry_rut.get()
        nombre = entry_nombre.get()
        direccion = entry_direccion.get()
        comuna = entry_comuna.get()
        correo = entry_correo.get()
        edad = entry_edad.get()
        celular = entry_celular.get()
        tipo = tipo_var.get()

        # Validaciones
        if not rut.isdigit() or len(rut) < 7:
            messagebox.showerror("Error", "Ingrese un RUT válido")
            return
        if "@" not in correo:
            messagebox.showerror("Error", "Correo no válido")
            return
        if not edad.isdigit() or int(edad) < 18:
            messagebox.showerror("Error", "Debe ser mayor de 18 años")
            return

        try:
            # Conexión a la base de datos SQLite
            conn = sqlite3.connect("clientes.db")
            cursor = conn.cursor()

            # Insertar datos en la tabla clientes
            cursor.execute("""
                INSERT INTO clientes (rut, nombre, direccion, comuna, correo, edad, celular, tipo)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (rut, nombre, direccion, comuna, correo, int(edad), celular, tipo))

            # Guardar cambios y cerrar conexión
            conn.commit()
            conn.close()

            messagebox.showinfo("Éxito", "Cliente registrado con éxito")
            cliente_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "El RUT ya está registrado")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {e}")

    # Interfaz gráfica
    cliente_window = tk.Toplevel()
    cliente_window.title("Registro de Cliente")

    tk.Label(cliente_window, text="RUT:").grid(row=0, column=0)
    entry_rut = tk.Entry(cliente_window)
    entry_rut.grid(row=0, column=1)

    tk.Label(cliente_window, text="Nombre:").grid(row=1, column=0)
    entry_nombre = tk.Entry(cliente_window)
    entry_nombre.grid(row=1, column=1)

    tk.Label(cliente_window, text="Dirección:").grid(row=2, column=0)
    entry_direccion = tk.Entry(cliente_window)
    entry_direccion.grid(row=2, column=1)

    tk.Label(cliente_window, text="Comuna:").grid(row=3, column=0)
    entry_comuna = tk.Entry(cliente_window)
    entry_comuna.grid(row=3, column=1)

    tk.Label(cliente_window, text="Correo:").grid(row=4, column=0)
    entry_correo = tk.Entry(cliente_window)
    entry_correo.grid(row=4, column=1)

    tk.Label(cliente_window, text="Edad:").grid(row=5, column=0)
    entry_edad = tk.Entry(cliente_window)
    entry_edad.grid(row=5, column=1)

    tk.Label(cliente_window, text="Celular:").grid(row=6, column=0)
    entry_celular = tk.Entry(cliente_window)
    entry_celular.grid(row=6, column=1)

    tk.Label(cliente_window, text="Tipo de Cliente:").grid(row=7, column=0)
    tipo_var = tk.StringVar(value="Habitual")
    tk.OptionMenu(cliente_window, tipo_var, "Preferencial", "Habitual", "Ocasional").grid(row=7, column=1)

    tk.Button(cliente_window, text="Registrar", command=guardar_cliente).grid(row=8, columnspan=2)



def habilitar_botones():
    btn_registrar_cliente.config(state="normal")
    btn_consultar_cliente.config(state="normal")
    btn_modificar_cliente.config(state="normal")
    btn_eliminar_cliente.config(state="normal")


def consultar_cliente():
    rut = simpledialog.askstring("Consultar Cliente", "Ingrese el RUT del cliente:")
    
    if not rut:
        return  # Si no se ingresa un RUT, salir de la función

    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clientes WHERE rut = ?", (rut,))
    cliente = cursor.fetchone()

    conn.close()

    if cliente:
        columnas = ["RUT", "Nombre", "Dirección", "Comuna", "Correo", "Edad", "Celular", "Tipo de Cliente"]
        mensaje = "\n".join(f"{col}: {val}" for col, val in zip(columnas, cliente))
        messagebox.showinfo("Información del Cliente", mensaje)
    else:
        messagebox.showerror("Error", "Cliente no encontrado")


# ✏ MODIFICAR CLIENTE
def modificar_cliente():
    rut = simpledialog.askstring("Modificar Cliente", "Ingrese el RUT del cliente:")
    
    if not rut:
        return  # Si no se ingresa un RUT, salir de la función

    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM clientes WHERE rut = ?", (rut,))
    cliente = cursor.fetchone()

    if not cliente:
        messagebox.showerror("Error", "Cliente no encontrado")
        conn.close()
        return

    conn.close()

    # Crear ventana para modificar los datos
    cliente_window = tk.Toplevel()
    cliente_window.title("Modificar Cliente")

    # Crear etiquetas y campos de entrada con los datos actuales del cliente
    campos = ["Nombre", "Dirección", "Comuna", "Correo", "Edad", "Celular"]
    entradas = {}

    for i, (campo, valor) in enumerate(zip(campos, cliente[1:])):  # Saltamos el RUT (cliente[0])
        tk.Label(cliente_window, text=f"{campo}:").grid(row=i, column=0)
        entrada = tk.Entry(cliente_window)
        entrada.insert(0, valor)  # Rellenar con el valor actual
        entrada.grid(row=i, column=1)
        entradas[campo] = entrada  # Guardar la referencia del campo

    def guardar_modificacion():
        nuevos_datos = {campo: entrada.get() for campo, entrada in entradas.items()}

        if "@" not in nuevos_datos["Correo"]:
            messagebox.showerror("Error", "Correo no válido")
            return
        
        if not nuevos_datos["Edad"].isdigit() or int(nuevos_datos["Edad"]) < 18:
            messagebox.showerror("Error", "Debe ser mayor de 18 años")
            return

        conn = sqlite3.connect("clientes.db")
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE clientes 
            SET nombre = ?, direccion = ?, comuna = ?, correo = ?, edad = ?, celular = ?
            WHERE rut = ?
        """, (nuevos_datos["Nombre"], nuevos_datos["Dirección"], nuevos_datos["Comuna"],
              nuevos_datos["Correo"], nuevos_datos["Edad"], nuevos_datos["Celular"], rut))

        conn.commit()
        conn.close()

        messagebox.showinfo("Éxito", "Cliente modificado con éxito")
        cliente_window.destroy()

    tk.Button(cliente_window, text="Guardar Cambios", command=guardar_modificacion).grid(row=len(campos), columnspan=2)

# ❌ ELIMINAR CLIENTE
def eliminar_cliente():
    rut = simpledialog.askstring("Eliminar Cliente", "Ingrese el RUT del cliente:")

    if not rut:
        return  # Si no se ingresa un RUT, salir de la función

    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()

    # Verificar si el cliente existe en la base de datos
    cursor.execute("SELECT nombre FROM clientes WHERE rut = ?", (rut,))
    cliente = cursor.fetchone()

    if not cliente:
        messagebox.showerror("Error", "Cliente no encontrado")
        conn.close()
        return

    # Confirmación antes de eliminar
    confirmacion = messagebox.askyesno("Confirmar", f"¿Seguro que desea eliminar al cliente {cliente[0]}?")
    
    if confirmacion:
        cursor.execute("DELETE FROM clientes WHERE rut = ?", (rut,))
        conn.commit()
        messagebox.showinfo("Éxito", "Cliente eliminado con éxito")
    
    conn.close()

def obtener_nombre_cliente(rut):
    conn = sqlite3.connect("clientes.db")  # Asegúrate de usar el nombre correcto
    cursor = conn.cursor()
    
    cursor.execute("SELECT nombre FROM clientes WHERE rut = ?", (rut,))
    resultado = cursor.fetchone()
    
    conn.close()
    
    # Si no se encuentra el cliente, devuelve None
    return resultado[0] if resultado else None


def registrar_pedido():
    # Pedir RUT del cliente antes de abrir la ventana de pedido
    rut = simpledialog.askstring("Registrar Pedido", "Ingrese el RUT del cliente:")
    
    # Si el usuario no ingresa nada o cancela, no abrir la ventana
    if not rut:
        messagebox.showerror("Error", "Debe ingresar un RUT válido")
        return

    # Obtener el nombre del cliente usando la función que creaste
    nombre_cliente = obtener_nombre_cliente(rut)
    
    # Imprimir el valor de nombre_cliente para depuración
    print(f"Nombre del cliente: '{nombre_cliente}'")

    # Verificar si el nombre del cliente es None o vacío (significa que no se encontró el cliente)
    if not nombre_cliente:
        messagebox.showerror("Error", "No se encuentra un cliente con ese RUT")
        return

    # Abrir la ventana de registro de pedido si el cliente existe
    pedido_window = tk.Toplevel(root)
    pedido_window.title(f"Registro de Pedido - {nombre_cliente}")  # Mostrar el nombre en el título

    productos = {"California": 5100, "Crab Ahumado": 6100, "Tempura": 5800}
    total = tk.IntVar(value=0)

    def agregar_pedido(producto, precio):
        try:
            cantidad = int(entry_cantidad.get())
            if cantidad <= 0:
                raise ValueError
            total.set(total.get() + (cantidad * precio))
            label_total.config(text=f"Total: ${total.get()}")
        except ValueError:
            messagebox.showerror("Error", "Ingrese una cantidad válida")

    # Mostrar nombre del cliente en la ventana
    tk.Label(pedido_window, text=f"Cliente: {nombre_cliente}", font=("Arial", 12, "bold")).grid(row=0, columnspan=2, pady=5)

    tk.Label(pedido_window, text="Cantidad:").grid(row=1, column=0)
    entry_cantidad = tk.Entry(pedido_window)
    entry_cantidad.grid(row=1, column=1)

    row = 2
    for producto, precio in productos.items():
        tk.Button(pedido_window, text=f"{producto} - ${precio}", 
                  command=lambda p=producto, pr=precio: agregar_pedido(p, pr)).grid(row=row, columnspan=2, pady=2)
        row += 1

    label_total = tk.Label(pedido_window, text="Total: $0", font=("Arial", 10, "bold"))
    label_total.grid(row=row, columnspan=2, pady=5)

    tk.Button(pedido_window, text="Cerrar", command=pedido_window.destroy).grid(row=row+1, columnspan=2, pady=5)


root = tk.Tk()
root.title("Sushi-Nikkey App")
clientes = {}
root.geometry("600x500")
label = tk.Label(root, text="¡Bienvenido a Sushi Nikkey!", font=("Arial", 14), bg="black", fg="white")
label.place(x=250, y=20)
labelmenu = tk.Label(root, text="Menu actual", font=("Arial", 14), bg="black", fg="white")
labelmenu.place(x=310, y=100)
labelproductos = tk.Label(root, text="California: $5.100 \n Crab Ahumado: $6.100 \n Tempura: $5.800", font=("Arial", 14), bg="black", fg="white")
labelproductos.place(x=255, y=180)
root.configure(bg="black")
root.minsize(600, 500)
root.maxsize(600, 500)


##logo
image = Image.open("logo.png").convert("RGBA") 
image = image.resize((100, 100))
photo = ImageTk.PhotoImage(image)
logo_label = tk.Label(root, image=photo)
logo_label.pack(pady=10)
logo_label.place(x=40, y=70)
logo_label.lift()


#botones
btn_registrar_cliente = tk.Button(root, text="Registrar Cliente", command=registrar_cliente, bg="blue", state="disabled")
btn_registrar_cliente.place(relx=0.15, rely=0.40, anchor="center", width=150, height=35)

btn_consultar_cliente = tk.Button(root, text="Consultar Cliente", command=consultar_cliente, bg="lightgreen", state="disabled")
btn_consultar_cliente.place(relx=0.15, rely=0.47, anchor="center", width=150, height=35)

btn_modificar_cliente = tk.Button(root, text="Modificar Cliente", command=modificar_cliente, bg="yellow", state="disabled")
btn_modificar_cliente.place(relx=0.15, rely=0.54, anchor="center", width=150, height=35)

btn_eliminar_cliente = tk.Button(root, text="Eliminar Cliente", command=eliminar_cliente, bg="red", fg="white", state="disabled")
btn_eliminar_cliente.place(relx=0.15, rely=0.61, anchor="center", width=150, height=35)

btn_registrar_pedido = tk.Button(root, text="Registrar Pedido", command=registrar_pedido, bg="orange")
btn_registrar_pedido.place(relx=0.15, rely=0.68, anchor="center", width=150, height=35)

btn_salir = tk.Button(root, text="Salir", command=root.quit, bg="red", fg="white")
btn_salir.place(relx=0.15, rely=0.75, anchor="center", width=150, height=35)

btn_login = tk.Button(root, text="Login Admin", command=login_admin, bg="white")
btn_login.place(relx=0.15, rely=0.08, anchor="center", width=150, height=35)


root.mainloop()
