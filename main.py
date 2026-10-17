import json
from pathlib import Path
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import tkinter as tk
import subprocess
import threading

# Configuración visual de TeoSoft
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

CARPETA_PROYECTO = Path(__file__).resolve().parent
ARCHIVO_CATALOGO = CARPETA_PROYECTO / "catalogo.json"


def cargar_catalogo():
    with open(ARCHIVO_CATALOGO, "r", encoding="utf-8") as archivo:
        return json.load(archivo)["programas"]


def instalador_disponible(programa):
    ruta = (CARPETA_PROYECTO / programa["archivo"]).resolve()

    # Evita rutas que intenten salir de la carpeta del proyecto.
    if not ruta.is_relative_to(CARPETA_PROYECTO):
        return False

    return ruta.is_file()


def programa_instalado(programa):
    """Comprueba si Chrome o Firefox están instalados en Windows."""

    nombre = programa["nombre"].lower()

    if nombre == "google chrome":
        posibles_rutas = [
            Path(
                r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            ),
            Path(
                r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
            ),
            Path(
                Path.home()
                / "AppData/Local/Google/Chrome/Application/chrome.exe"
            ),
        ]

        return any(ruta.is_file() for ruta in posibles_rutas)

    if nombre == "mozilla firefox":
        posibles_rutas = [
            Path(r"C:\Program Files\Mozilla Firefox\firefox.exe"),
            Path(r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"),
            Path(
                Path.home()
                / "AppData/Local/Mozilla Firefox/firefox.exe"
            ),
        ]

        return any(ruta.is_file() for ruta in posibles_rutas)


    if nombre == "brave browser":
        posibles_rutas = [
            Path(
                r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
            ),
            Path(
                r"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe"
            ),
            Path(
                Path.home()
                / "AppData/Local/BraveSoftware/Brave-Browser/Application/brave.exe"
            ),
        ]

        return any(ruta.is_file() for ruta in posibles_rutas)

    if nombre == "vlc media player":
        posibles_rutas = [
            Path(r"C:\Program Files\VideoLAN\VLC\vlc.exe"),
            Path(r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe"),
        ]
        return any(ruta.is_file() for ruta in posibles_rutas)

    if nombre == "7-zip":
        posibles_rutas = [
            Path(r"C:\Program Files\7-Zip\7zFM.exe"),
            Path(r"C:\Program Files\7-Zip\7z.exe"),
            Path(r"C:\Program Files (x86)\7-Zip\7zFM.exe"),
            Path(r"C:\Program Files (x86)\7-Zip\7z.exe"),
        ]
        return any(ruta.is_file() for ruta in posibles_rutas)


    if nombre == "adobe acrobat reader":
        posibles_rutas = [
            Path(r"C:\Program Files\Adobe\Acrobat DC\Acrobat\Acrobat.exe"),
            Path(r"C:\Program Files (x86)\Adobe\Acrobat DC\Acrobat\Acrobat.exe"),
            Path(r"C:\Program Files\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe"),
            Path(r"C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe"),
        ]
        return any(ruta.is_file() for ruta in posibles_rutas)


    # Para programas que todavía no configuramos,
    # no afirmamos que estén instalados.
    return False

def seleccionar_disponibles():
    """Marca programas disponibles que todavía no están instalados."""
    for nombre, variable in seleccionados.items():
        programa = next(
            (p for p in programas if p["nombre"] == nombre),
            None
        )

        if programa is not None:
            disponible = instalador_disponible(programa)
            instalado = programa_instalado(programa)

            variable.set(disponible and not instalado)

def limpiar_seleccion():
    """Desmarca todos los programas."""
    for variable in seleccionados.values():
        variable.set(False)


def mostrar_seleccion():
    lista = [
        nombre
        for nombre, variable in seleccionados.items()
        if variable.get()
    ]

    if lista:
        mensaje = "Programas seleccionados:\n\n" + "\n".join(lista)
    else:
        mensaje = "No has seleccionado ningún programa."

    messagebox.showinfo("TeoSoft TechInstall", mensaje)



def instalar_programas():
    """Instala los programas seleccionados con una ventana de progreso."""

    programas_seleccionados = [
        programa
        for programa in programas
        if seleccionados[programa["nombre"]].get()
    ]

    if not programas_seleccionados:
        messagebox.showwarning(
            "TeoSoft TechInstall",
            "Selecciona al menos un programa.",
            parent=ventana
        )
        return

    confirmacion = messagebox.askyesno(
        "Confirmar instalación",
        f"Se instalarán {len(programas_seleccionados)} programa(s).\n\n"
        "¿Deseas continuar?",
        parent=ventana
    )

    if not confirmacion:
        return

    # Ventana de progreso
    progreso = ctk.CTkToplevel(ventana)
    progreso.title("TeoSoft - Instalando programas")
    progreso.geometry("540x470")
    progreso.resizable(False, False)
    progreso.transient(ventana)
    progreso.grab_set()

    progreso.protocol("WM_DELETE_WINDOW", lambda: None)

    ctk.CTkLabel(
        progreso,
        text="TeoSoft",
        font=("Segoe UI", 25, "bold")
    ).pack(pady=(22, 2))

    ctk.CTkLabel(
        progreso,
        text="INSTALACIÓN DE PROGRAMAS",
        font=("Segoe UI", 11),
        text_color="#48A9FF"
    ).pack(pady=(0, 20))

    nombre_actual = ctk.CTkLabel(
        progreso,
        text="Preparando instalación...",
        font=("Segoe UI", 15, "bold"),
        wraplength=480
    )
    nombre_actual.pack(pady=(0, 6))

    estado_actual = ctk.CTkLabel(
        progreso,
        text="Iniciando...",
        text_color="#AAB6C8"
    )
    estado_actual.pack(pady=(0, 12))

    ctk.CTkLabel(
        progreso,
        text="Progreso general",
        font=("Segoe UI", 12, "bold")
    ).pack(anchor="w", padx=30)

    barra_general = ctk.CTkProgressBar(
        progreso,
        height=12,
        progress_color="#2589F5"
    )
    barra_general.pack(fill="x", padx=30, pady=(7, 5))
    barra_general.set(0)

    texto_progreso = ctk.CTkLabel(
        progreso,
        text=f"0 de {len(programas_seleccionados)} programas completados"
    )
    texto_progreso.pack(anchor="e", padx=30, pady=(0, 15))

    ctk.CTkLabel(
        progreso,
        text="Actividad",
        font=("Segoe UI", 12, "bold")
    ).pack(anchor="w", padx=30, pady=(0, 5))

    registro = ctk.CTkTextbox(
        progreso,
        height=125,
        corner_radius=8,
        font=("Consolas", 11)
    )
    registro.pack(fill="both", expand=True, padx=30, pady=(0, 12))
    registro.configure(state="disabled")

    boton_cerrar = ctk.CTkButton(
        progreso,
        text="Instalando...",
        state="disabled",
        command=progreso.destroy
    )
    boton_cerrar.pack(pady=(0, 18))

    barra_actual = ctk.CTkProgressBar(
        progreso,
        mode="indeterminate",
        height=5,
        progress_color="#48A9FF"
    )
    # La barra animada se coloca debajo del estado.
    barra_actual.pack(fill="x", padx=30, pady=(0, 12), before=nombre_actual)
    barra_actual.start()

    if "boton_instalar" in globals():
        boton_instalar.configure(state="disabled")

    def agregar_registro(mensaje):
        registro.configure(state="normal")
        registro.insert("end", mensaje + "\n")
        registro.see("end")
        registro.configure(state="disabled")

    def preparar_programa(nombre, numero):
        nombre_actual.configure(text=nombre)
        estado_actual.configure(text="Ejecutando instalador...")
        texto_progreso.configure(
            text=f"Programa {numero} de {len(programas_seleccionados)}"
        )
        barra_actual.start()

    def actualizar_resultado(mensaje, numero, nombre, requiere_reinicio=False):
        barra_actual.stop()
        agregar_registro(mensaje)
        
        etiqueta = estados_programas.get(nombre)

        if etiqueta:
            if mensaje.startswith("OK:") or mensaje.startswith("OMITIDO:"):
                etiqueta.configure(
                    text="Ya instalado",
                    text_color="#4ADE80"
                )
            elif mensaje.startswith("ERROR:"):
                etiqueta.configure(
                    text="Error",
                    text_color="#F87171"
                )

        nombre_actual.configure(text=nombre)
        estado_actual.configure(
            text="Proceso terminado. Se requiere reiniciar Windows."
            if requiere_reinicio
            else "Programa procesado."
        )
        barra_general.set(numero / len(programas_seleccionados))
        texto_progreso.configure(
            text=f"{numero} de {len(programas_seleccionados)} programas procesados"
        )

    def finalizar_instalaciones():
        barra_actual.stop()
        barra_general.set(1)
        nombre_actual.configure(text="Proceso finalizado")
        estado_actual.configure(
            text="Revisa el registro para ver los resultados."
        )
        boton_cerrar.configure(
            text="Cerrar",
            state="normal",
            command=progreso.destroy
        )

        # Permitir cerrar la ventana cuando termine la instalación.
        progreso.protocol("WM_DELETE_WINDOW", progreso.destroy)

        if "boton_instalar" in globals():
            boton_instalar.configure(state="normal")

    def ejecutar_instalaciones():
        resultados = []
        total = len(programas_seleccionados)

        for numero, programa in enumerate(programas_seleccionados, start=1):
            nombre = programa["nombre"]

            ventana.after(
                0,
                lambda n=nombre, i=numero: preparar_programa(n, i)
            )

            # Omitir programas que ya están instalados.
            if programa_instalado(programa):
                mensaje = f"OMITIDO: {nombre} ya está instalado."
                resultados.append(mensaje)

                ventana.after(
                    0,
                    lambda m=mensaje, i=numero, n=nombre:
                        actualizar_resultado(m, i, n)
                )
                continue

            # Comprobar que el instalador exista.
            if not instalador_disponible(programa):
                mensaje = f"ERROR: {nombre}: instalador no encontrado."
                resultados.append(mensaje)

                ventana.after(
                    0,
                    lambda m=mensaje, i=numero, n=nombre:
                        actualizar_resultado(m, i, n)
                )
                continue

            ruta = CARPETA_PROYECTO / programa["archivo"]
            argumentos = programa.get("argumentos", [])

            try:
                if ruta.suffix.lower() == ".msi":
                    comando = [
                        "msiexec.exe",
                        "/i",
                        str(ruta),
                        *argumentos
                    ]
                else:
                    comando = [
                        str(ruta),
                        *argumentos
                    ]

                resultado = subprocess.run(
                    comando,
                    check=False
                )

                if resultado.returncode == 0:
                    mensaje = f"OK: {nombre}: instalación finalizada."
                    reinicio = False
                elif resultado.returncode in (3010, 1641):
                    mensaje = (
                        f"OK: {nombre}: instalación finalizada; "
                        "se requiere reiniciar Windows."
                    )
                    reinicio = True
                else:
                    mensaje = (
                        f"ERROR: {nombre}: código de salida "
                        f"{resultado.returncode}."
                    )
                    reinicio = False

            except Exception as error:
                mensaje = f"ERROR: {nombre}: {error}"
                reinicio = False

            resultados.append(mensaje)

            ventana.after(
                0,
                lambda m=mensaje, i=numero, n=nombre, r=reinicio:
                    actualizar_resultado(m, i, n, r)
            )

        ventana.after(0, finalizar_instalaciones)

    threading.Thread(
        target=ejecutar_instalaciones,
        daemon=True
    ).start()



# Ventana principal
ventana = ctk.CTk()
ventana.title("TeoSoft - TechInstall")
ventana.geometry("780x700")
ventana.minsize(680, 600)

# Icono personalizado de TeoSoft para Windows
RUTA_ICONO = CARPETA_PROYECTO / "assets" / "teosoft_logo.ico"

if RUTA_ICONO.is_file():
    ventana.iconbitmap(str(RUTA_ICONO))

# Icono de la ventana
RUTA_ICONO = CARPETA_PROYECTO / "assets" / "teosoft_logo.png"

try:
    icono = tk.PhotoImage(file=str(RUTA_ICONO))
    ventana.iconphoto(True, icono)
except Exception as error:
    print(f"No se pudo cargar el icono: {error}")

# Encabezado
encabezado = ctk.CTkFrame(ventana, fg_color="transparent")
encabezado.pack(fill="x", padx=28, pady=(25, 15))

# Logotipo de TeoSoft
RUTA_LOGO = CARPETA_PROYECTO / "assets" / "teosoft_logo.png"

imagen_logo = ctk.CTkImage(
    light_image=Image.open(RUTA_LOGO),
    dark_image=Image.open(RUTA_LOGO),
    size=(76, 76)
)

logo = ctk.CTkLabel(
    encabezado,
    text="",
    image=imagen_logo
)
logo.pack(side="left", padx=(0, 16))

marca = ctk.CTkFrame(encabezado, fg_color="transparent")
marca.pack(side="left", fill="y")

ctk.CTkLabel(
    marca,
    text="TeoSoft",
    font=("Segoe UI", 27, "bold")
).pack(anchor="w")

ctk.CTkLabel(
    marca,
    text="TECHINSTALL  •  SOPORTE TÉCNICO OFFLINE",
    font=("Segoe UI", 11),
    text_color="#48A9FF"
).pack(anchor="w", pady=(3, 0))

programas = cargar_catalogo()

RUTA_ICONOS = CARPETA_PROYECTO / "assets" / "programas"

ICONOS_PROGRAMAS = {
    "Google Chrome": "google.png",
    "Mozilla Firefox": "firefox.png",
    "Brave Browser": "brave.png",
    "VLC Media Player": "VLC.png",
    "7-Zip": "7zip.png",
    "Adobe Acrobat Reader": "adobe.png",
}

seleccionados = {}

# Categorías disponibles en el catálogo
categorias = ["Todos"] + sorted({
    programa["categoria"]
    for programa in programas
})


# Buscador de programas
barra_busqueda = ctk.CTkFrame(
    ventana,
    fg_color="transparent"
)
barra_busqueda.pack(fill="x", padx=30, pady=(4, 12))

ctk.CTkLabel(
    barra_busqueda,
    text="Buscar programa",
    font=("Segoe UI", 12, "bold"),
    text_color="#D1D5DB"
).pack(anchor="w", pady=(0, 6))

entrada_busqueda = ctk.CTkEntry(
    barra_busqueda,
    placeholder_text="Escribe el nombre de una aplicación...",
    height=40,
    corner_radius=10,
    border_color="#303744",
    fg_color="#171B22",
    font=("Segoe UI", 13)
)
entrada_busqueda.pack(fill="x")



# Barra de pestañas para filtrar categorías
categoria_actual = ctk.StringVar(value="Todos")


# Título de sección
ctk.CTkLabel(
    ventana,
    text="Selecciona los programas",
    font=("Segoe UI", 20, "bold")
).pack(anchor="w", padx=30, pady=(12, 4))

ctk.CTkLabel(
    ventana,
    text="Marca las aplicaciones que deseas instalar en el equipo.",
    text_color="#A8B0BD",
    font=("Segoe UI", 12)
).pack(anchor="w", padx=30, pady=(0, 16))

barra_categorias = ctk.CTkFrame(
    ventana,
    fg_color="transparent"
)
barra_categorias.pack(fill="x", padx=25, pady=(0, 10))

for categoria in categorias:
    ctk.CTkButton(
        barra_categorias,
        text=categoria,
        width=110,
        height=34,
        corner_radius=8,
        command=lambda c=categoria: categoria_actual.set(c)
    ).pack(side="left", padx=3)


# Acciones rápidas de selección
barra_acciones = ctk.CTkFrame(
    ventana,
    fg_color="transparent"
)
barra_acciones.pack(fill="x", padx=25, pady=(0, 10))

ctk.CTkButton(
    barra_acciones,
    text="✓  Seleccionar disponibles",
    height=36,
    corner_radius=8,
    fg_color="#16803D",
    hover_color="#11632F",
    font=("Segoe UI", 12, "bold"),
    command=seleccionar_disponibles
).pack(side="left", padx=(0, 8))

ctk.CTkButton(
    barra_acciones,
    text="✕  Limpiar selección",
    height=36,
    corner_radius=8,
    fg_color="#374151",
    hover_color="#4B5563",
    font=("Segoe UI", 12),
    command=limpiar_seleccion
).pack(side="left")


# Botón para instalar los programas seleccionados
boton_instalar = ctk.CTkButton(
    barra_acciones,
    text="▶  Instalar seleccionados",
    height=36,
    corner_radius=8,
    fg_color="#2563EB",
    hover_color="#1D4ED8",
    font=("Segoe UI", 12, "bold"),
    command=instalar_programas
)

boton_instalar.pack(side="right")


# Catálogo
marco = ctk.CTkFrame(
    ventana,
    corner_radius=16,
    fg_color="#171B22",
    border_width=1,
    border_color="#303744"
)
marco.pack(fill="both", expand=True, padx=25, pady=5)

# Guardamos las filas para poder filtrarlas
filas_programas = []


# Guardamos las etiquetas de estado para actualizarlas después.
estados_programas = {}

for programa in programas:
    nombre = programa["nombre"]
    categoria = programa["categoria"]
    disponible = instalador_disponible(programa)
    instalado = programa_instalado(programa)

    fila = ctk.CTkFrame(
        marco,
        fg_color="#202630",
        corner_radius=10
    )
    fila.pack(fill="x", padx=14, pady=(12, 0))

    variable = ctk.BooleanVar(value=False)

    # Cargar y mostrar el icono del programa.
    archivo_icono = ICONOS_PROGRAMAS.get(nombre)
    ruta_icono = RUTA_ICONOS / archivo_icono if archivo_icono else None

    if ruta_icono and ruta_icono.is_file():
        imagen_original = Image.open(ruta_icono).convert("RGBA")
        imagen_original.thumbnail((36, 36))

        icono_programa = ctk.CTkImage(
            light_image=imagen_original,
            dark_image=imagen_original,
            size=imagen_original.size
        )

        etiqueta_icono = ctk.CTkLabel(
         fila,
            text="",
            image=icono_programa
        )
        etiqueta_icono.pack(side="left", padx=(14, 8))

    # Evitar que la imagen sea liberada por el recolector.
        etiqueta_icono.image = icono_programa

    casilla = ctk.CTkCheckBox(
        fila,
        text=nombre,
        variable=variable,
        font=("Segoe UI", 14),
        checkbox_width=22,
        checkbox_height=22,
        state="disabled" if instalado or not disponible else "normal"
    )
    casilla.pack(side="left", padx=16, pady=16)

    if instalado:
        estado = "Ya instalado"
        color_estado = "#4ADE80"
    elif disponible:
        estado = "Disponible"
        color_estado = "#60A5FA"
    else:
        estado = "Instalador pendiente"
        color_estado = "#9CA3AF"

    etiqueta_estado = ctk.CTkLabel(
        fila,
        text=estado,
        text_color=color_estado,
        font=("Segoe UI", 11)
    )
    etiqueta_estado.pack(side="right", padx=(5, 14))

    estados_programas[nombre] = etiqueta_estado

    ctk.CTkLabel(
        fila,
        text=categoria,
        text_color="#48A9FF",
        font=("Segoe UI", 11)
    ).pack(side="right", padx=8)

    seleccionados[nombre] = variable

    filas_programas.append({
        "fila": fila,
        "categoria": categoria
    })



# Conectar los botones de categorías
botones_categorias = {}

for boton in barra_categorias.winfo_children():
    categoria = boton.cget("text")
    botones_categorias[categoria] = boton

    boton.configure(
        command=lambda c=categoria: filtrar_categoria(c)
    )


# Actualizar el aspecto de la categoría activa
def actualizar_estilo_categorias(categoria_activa):
    for categoria, boton in botones_categorias.items():
        if categoria == categoria_activa:
            boton.configure(
                fg_color="#0B5CAD",
                hover_color="#084A8C",
                text_color="#FFFFFF"
            )
        else:
            boton.configure(
                fg_color="#246BA8",
                hover_color="#18558A",
                text_color="#FFFFFF"
            )

# Filtrar y resaltar la pestaña seleccionada
def filtrar_categoria(categoria):
    categoria_actual.set(categoria)

    for elemento in filas_programas:
        fila = elemento["fila"]
        categoria_programa = elemento["categoria"]

        if categoria == "Todos" or categoria_programa == categoria:
            fila.pack(fill="x", padx=14, pady=(12, 0))
        else:
            fila.pack_forget()

    actualizar_estilo_categorias(categoria)


# Buscar programas por nombre
def buscar_programas(*args):
    texto = entrada_busqueda.get().strip().casefold()
    categoria = categoria_actual.get()

    for elemento in filas_programas:
        fila = elemento["fila"]
        nombre = fila.winfo_children()[0].cget("text").casefold()
        categoria_programa = elemento["categoria"]

        coincide_nombre = texto in nombre
        coincide_categoria = (
            categoria == "Todos"
            or categoria_programa == categoria
        )

        if coincide_nombre and coincide_categoria:
            fila.pack(fill="x", padx=14, pady=(12, 0))
        else:
            fila.pack_forget()

# Conectar el buscador cuando la función ya está definida
entrada_busqueda.bind("<KeyRelease>", buscar_programas)

# Botón principal
ctk.CTkButton(
    ventana,
    text="Ver selección",
    height=46,
    corner_radius=10,
    font=("Segoe UI", 14, "bold"),
    command=mostrar_seleccion
).pack(pady=18)

# Mensaje inferior
ctk.CTkLabel(
    ventana,
    text="Las casillas se habilitan cuando el instalador está disponible.",
    text_color="#8DBFEF",
    font=("Segoe UI", 11)
).pack(pady=(0, 18))

ventana.mainloop()
