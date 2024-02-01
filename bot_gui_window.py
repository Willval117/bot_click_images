import tkinter as tk
from tkinter import filedialog
import pyautogui as pt
from time import sleep

def es_flotante(P):
    if P == "":
        return True 
    try:
        float(P)
        return True
    except ValueError:
        return False

def seleccionar_archivo(entrada_ruta):
    ruta_archivo = filedialog.askopenfilename()
    entrada_ruta.config(state=tk.NORMAL)
    entrada_ruta.delete(0, tk.END)
    entrada_ruta.insert(0, ruta_archivo)
    entrada_ruta.config(state='readonly')

def guardar_todo():
    retardo = entrada_retardo.get()
    n_veces = entrada_n_veces.get()
    vel_glo = entrada_velocidad_glo.get()
    ejec_automaticamente = check_ejecutar_var.get() == 1
    repeticion = check_repetir_var.get() == 1
    try:
        with open('conf.txt', 'w') as archivo_conf:
            archivo_conf.write(f"{ejec_automaticamente},{retardo},{repeticion},{n_veces},{vel_glo}\n")
        print("Configuración guardada con éxito.")
    except Exception as e:
        print("Error al guardar la configuración:", e)
    
    # Guardar rutas y datos en rutas.txt
    try:
        with open('rutas.txt', 'w') as archivo_txt:
            for i, entrada in enumerate(entradas, start=1):
                ruta = entrada[0].get()
                tiempo = entrada[1].get()
                velocidad = entrada[2].get()
                x = entrada[3].get()
                y = entrada[4].get()
                archivo_txt.write(f"{i}, {ruta}, {tiempo}, {velocidad}, {x}, {y}\n")
        print("Datos guardados con éxito.")
    except Exception as e:
        print("Error al guardar los datos:", e)

def eliminar_linea(entrada_ruta):
    for fila in entradas:
        if fila[0] is entrada_ruta:
            for widget in fila:
                widget.destroy()
            entradas.remove(fila)
            break

def agregar_linea(datos=None):
    validador = ventana.register(es_flotante)
    
    entrada_ruta = tk.Entry(frame_scrollable, width=50)
    entrada_ruta.config(state=tk.NORMAL)
    entrada_tiempo = tk.Entry(frame_scrollable, width=20, validate="key", validatecommand=(validador, '%P'))
    entrada_velocidad = tk.Entry(frame_scrollable, width=20, validate="key", validatecommand=(validador, '%P'))
    entrada_x = tk.Entry(frame_scrollable, width=10, validate="key", validatecommand=(validador, '%P'))
    entrada_y = tk.Entry(frame_scrollable, width=10, validate="key", validatecommand=(validador, '%P'))
    boton_seleccionar = tk.Button(frame_scrollable, text="Seleccionar Archivo", command=lambda: seleccionar_archivo(entrada_ruta))
    boton_eliminar = tk.Button(frame_scrollable, text="Eliminar", command=lambda: eliminar_linea(entrada_ruta))
    entradas.append([entrada_ruta, entrada_tiempo, entrada_velocidad,entrada_x, entrada_y,boton_seleccionar, boton_eliminar])

    if datos:
        entrada_ruta.insert(0, datos[0])
        entrada_tiempo.insert(0, datos[1])
        entrada_velocidad.insert(0, datos[2])
        entrada_x.insert(0, datos[3])
        entrada_y.insert(0, datos[4])
    entrada_ruta.config(state='readonly')

    entrada_ruta.grid(row=len(entradas), column=0)
    entrada_tiempo.grid(row=len(entradas), column=1)
    entrada_velocidad.grid(row=len(entradas), column=2)
    entrada_x.grid(row=len(entradas), column=3)
    entrada_y.grid(row=len(entradas), column=4)
    boton_seleccionar.grid(row=len(entradas), column=5)
    boton_eliminar.grid(row=len(entradas), column=6)

def cargar_datos():
    try:
        with open('rutas.txt', 'r') as archivo_txt:
            for linea in archivo_txt:
                partes = linea.strip().split(", ")
                if len(partes) >= 6:  
                    agregar_linea(datos=partes[1:]) 
    except FileNotFoundError:
        print("El archivo rutas.txt no existe. Iniciando con una interfaz vacía.")

def cargar_configuracion():
    try:
        with open('conf.txt', 'r') as archivo_conf:
            lineas = archivo_conf.readline().strip()
            ejec_automaticamente, retardo, repeticion, n_veces, vel_glo = lineas.split(',')
            check_ejecutar_var.set(1 if ejec_automaticamente == 'True' else 0)
            check_repetir_var.set(1 if repeticion == 'True' else 0)
            entrada_retardo.insert(0, retardo)
            entrada_n_veces.insert(0, n_veces)
            entrada_velocidad_glo.insert(0,vel_glo)
    except FileNotFoundError:
        print("El archivo conf.txt no existe. Se iniciará con configuración predeterminada.")

def toggle_ejecutar():
    global ejecutar_automaticamente
    ejecutar_automaticamente = not ejecutar_automaticamente

def toggle_repetir():
    global repetir
    repetir = not repetir

def leer_configuracion():
    try:
        with open('conf.txt', 'r') as archivo_conf:
            lineas = archivo_conf.readline().strip()
            ejec_automaticamente, retardo, repeticion, n_veces, vel_glo = lineas.split(',')
            return {
                "ejec_automaticamente": ejec_automaticamente == 'True',
                "retardo": float(retardo),
                "repeticion": repeticion == 'True',
                "n_veces": int(n_veces),
                "vel_glo": float(vel_glo)
            }
    except FileNotFoundError:
        print("El archivo conf.txt no existe. Se iniciará con configuración predeterminada.")
        return None
    
def leer_rutas():
    rutas = []
    try:
        with open('rutas.txt', 'r') as archivo_txt:
            for linea in archivo_txt:
                partes = linea.strip().split(", ")
                if len(partes) >= 6:
                    rutas.append({
                        "ruta": partes[1],
                        "tiempo": float(partes[2]),
                        "velocidad": float(partes[3]),
                        "x": int(partes[4]),
                        "y": int(partes[5])
                    })
    except FileNotFoundError:
        print("El archivo rutas.txt no existe.")
    return rutas

def ejecutar_automatizacion():
    configuracion = leer_configuracion()
    if configuracion is None:
        return

    rutas = leer_rutas()
    if not rutas:
        print("No hay rutas para procesar.")
        return

    for _ in range(configuracion["n_veces"] if configuracion["repeticion"] else 1):
        for ruta in rutas:
            try:
                sleep(ruta["tiempo"])
                position = pt.locateOnScreen(ruta["ruta"], confidence=.7)
                pt.moveTo(position[0:2], duration=ruta["velocidad"])
                pt.moveRel(ruta["x"], ruta["y"], duration=ruta["velocidad"]) 
                pt.click(interval=configuracion["vel_glo"])
                
            except Exception as e:
                print('Error en la automatización:', e)
        sleep(configuracion["retardo"])

# WIDGET
ventana = tk.Tk()
ventana.title("Seleccionar etapas")
ventana.geometry("890x400")

#scrollbar
frame_scroll = tk.Frame(ventana)
frame_scroll.pack(fill=tk.BOTH, expand=True)

canvas = tk.Canvas(frame_scroll)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(frame_scroll, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar.set)

frame_scrollable = tk.Frame(canvas)
canvas.create_window((0, 0), window=frame_scrollable, anchor='nw')

entradas = []
ejecutar_automaticamente = False
repetir = False

#títulos de las columnas
label_ruta = tk.Label(frame_scrollable, text="Ruta", font=("Arial", 10, "bold"))
label_ruta.grid(row=0, column=0)
label_tiempo = tk.Label(frame_scrollable, text="Tiempo", font=("Arial", 10, "bold"))
label_tiempo.grid(row=0, column=1)
label_velocidad = tk.Label(frame_scrollable, text="Velocidad", font=("Arial", 10, "bold"))
label_velocidad.grid(row=0, column=2)
label_x = tk.Label(frame_scrollable, text="X", font=("Arial", 10, "bold"))
label_x.grid(row=0, column=3) 
label_y = tk.Label(frame_scrollable, text="Y", font=("Arial", 10, "bold"))
label_y.grid(row=0, column=4) 


# Pie de ventana
boton_guardar = tk.Button(ventana, text="Guardar BOT", command=guardar_todo)
boton_guardar.pack(side=tk.RIGHT, anchor=tk.NE)

boton_nueva_linea = tk.Button(ventana, text="Agregar Nueva Línea", command=agregar_linea)
boton_nueva_linea.pack(side=tk.RIGHT, anchor=tk.NE)

boton_ejecuta_test = tk.Button(ventana, text="Run Test", command=ejecutar_automatizacion)
boton_ejecuta_test.pack(side=tk.RIGHT, anchor=tk.NE)

frame_inferior = tk.Frame(ventana)
frame_inferior.pack(side=tk.BOTTOM, fill=tk.X)

check_ejecutar_var = tk.IntVar()
check_ejecutar = tk.Checkbutton(frame_inferior, text="Ejecutar Automáticamente.", variable=check_ejecutar_var)
check_ejecutar.pack(side=tk.LEFT)

label_retardo = tk.Label(frame_inferior, text="Retardo")
label_retardo.pack(side=tk.LEFT)
validador_flotante = ventana.register(es_flotante)
entrada_retardo = tk.Entry(frame_inferior, width=10, validate="key", validatecommand=(validador_flotante, '%P'))
entrada_retardo.pack(side=tk.LEFT)

check_repetir_var = tk.IntVar()
check_repetir = tk.Checkbutton(frame_inferior, text="Repetir.",  variable=check_repetir_var)
check_repetir.pack(side=tk.LEFT)

label_veces = tk.Label(frame_inferior, text="N. veces")
label_veces.pack(side=tk.LEFT)
validador_flotante = ventana.register(es_flotante)
entrada_n_veces = tk.Entry(frame_inferior, width=10, validate="key", validatecommand=(validador_flotante, '%P'))
entrada_n_veces.pack(side=tk.LEFT)

label_velocidad_global = tk.Label(frame_inferior, text="Velocidad")
label_velocidad_global.pack(side=tk.LEFT)
validador_flotante = ventana.register(es_flotante)
entrada_velocidad_glo = tk.Entry(frame_inferior, width=10, validate="key", validatecommand=(validador_flotante, '%P'))
entrada_velocidad_glo.pack(side=tk.LEFT)

#Cargar datos
cargar_datos()
cargar_configuracion()

def configurar_scroll_region(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame_scrollable.bind("<Configure>", configurar_scroll_region)

ventana.mainloop()
