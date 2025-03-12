import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk

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
        
        if not rut.isdigit() or len(rut) < 7:
            messagebox.showerror("Error", "Ingrese un RUT válido")
            return
        
        if "@" not in correo:
            messagebox.showerror("Error", "Correo no válido")
            return
        
        if not edad.isdigit() or int(edad) < 18:
            messagebox.showerror("Error", "Debe ser mayor de 18 años")
            return
        
        clientes[rut] = {
            "Nombre": nombre,
            "Dirección": direccion,
            "Comuna": comuna,
            "Correo": correo,
            "Edad": edad,
            "Celular": celular,
            "Tipo": tipo,
        }
        messagebox.showinfo("Éxito", "Cliente registrado con éxito")
        cliente_window.destroy()
    
    cliente_window = tk.Toplevel(root)
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

def consultar_cliente():
    rut = simpledialog.askstring("Consultar Cliente", "Ingrese el RUT del cliente:")
    if rut in clientes:
        info = clientes[rut]
        mensaje = "\n".join(f"{k}: {v}" for k, v in info.items())
        messagebox.showinfo("Información del Cliente", mensaje)
    else:
        messagebox.showerror("Error", "Cliente no encontrado")

def registrar_pedido():
    pedido_window = tk.Toplevel(root)
    pedido_window.title("Registro de Pedido")
    
    productos = {"California": 5100, "Crab Ahumado": 6100, "Tempura": 5800}
    total = tk.IntVar(value=0)
    
    def agregar_pedido(producto, precio):
        cantidad = int(entry_cantidad.get())
        total.set(total.get() + (cantidad * precio))
        label_total.config(text=f"Total: ${total.get()}")
    
    tk.Label(pedido_window, text="Cantidad:").grid(row=0, column=0)
    entry_cantidad = tk.Entry(pedido_window)
    entry_cantidad.grid(row=0, column=1)
    
    row = 1
    for producto, precio in productos.items():
        tk.Button(pedido_window, text=f"{producto} - ${precio}", command=lambda p=producto, pr=precio: agregar_pedido(p, pr)).grid(row=row, columnspan=2)
        row += 1
    
    label_total = tk.Label(pedido_window, text="Total: $0")
    label_total.grid(row=row, columnspan=2)
    
    tk.Button(pedido_window, text="Cerrar", command=pedido_window.destroy).grid(row=row+1, columnspan=2)



root = tk.Tk()
root.title("Sushi-Nikkey App")
clientes = {}
root.geometry("600x500")
label = tk.Label(root, text="¡Bienvenido a sushi nikkey!", font=("Arial", 14))
label.pack(pady=20)

##logo
image = Image.open("logo.png")
image = image.resize((100, 100))
photo = ImageTk.PhotoImage(image)
logo_label = tk.Label(root, image=photo)
logo_label.pack(pady=10)


tk.Button(root, text="Registrar Cliente", command=registrar_cliente).pack()
tk.Button(root, text="Consultar Cliente", command=consultar_cliente).pack()
tk.Button(root, text="Registrar Pedido", command=registrar_pedido).pack()
tk.Button(root, text="Salir", command=root.quit).pack()

root.mainloop()
