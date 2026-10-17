# TechInstall — TeoSoft

**Instalador de programas para soporte técnico en Windows**

TechInstall es una aplicación de escritorio desarrollada en Python que facilita la selección e instalación de programas utilizados habitualmente en tareas de soporte técnico y mantenimiento de equipos.

El proyecto busca simplificar la preparación de computadoras mediante una interfaz gráfica organizada por categorías, detección de aplicaciones instaladas y ejecución de instaladores disponibles.

## Características

- **Interfaz gráfica:** diseñada con CustomTkinter.
- **Catálogo por categorías:** navegadores, multimedia, PDF y utilidades.
- **Selección de programas:** permite seleccionar aplicaciones individualmente o seleccionar las disponibles.
- **Instalación automatizada:** ejecuta los instaladores con los argumentos configurados.
- **Detección de programas instalados:** identifica determinadas aplicaciones y actualiza su estado en la interfaz.
- **Búsqueda de programas:** facilita encontrar aplicaciones en el catálogo.
- **Indicador de progreso:** muestra el avance y los resultados de la instalación.
- **Identidad visual:** interfaz personalizada con la marca TeoSoft.

## Tecnologías utilizadas

- Python
- CustomTkinter
- Tkinter
- Pillow
- JSON
- Git y GitHub

## Estructura del proyecto

```text
TechInstall/
├── assets/
│   ├── programas/
│   ├── teosoft_logo.png
│   └── teosoft_logo.ico
├── Instaladores/
│   ├── Multimedia/
│   ├── Navegadores/
│   ├── PDF/
│   └── Utilidades/
├── .gitignore
├── catalogo.json
├── main.py
└── README.md
```

**Nota:** la carpeta `Instaladores/` se mantiene fuera del repositorio público para evitar subir ejecutables de gran tamaño. Cada usuario debe obtener los instaladores que necesite desde sus fuentes oficiales y colocarlos en las rutas correspondientes.

## Requisitos

- Windows
- Python 3
- pip

## Instalación y ejecución

1. Clona el repositorio:

   ```bash
   git clone https://github.com/TeoWebs/TechInstall.git
   ```

2. Accede a la carpeta:

   ```bash
   cd TechInstall
   ```

3. Instala las dependencias:

   ```bash
   py -m pip install customtkinter pillow
   ```

4. Coloca los instaladores correspondientes en sus carpetas dentro de `Instaladores/`, respetando las rutas y los nombres definidos en `catalogo.json`.

5. Ejecuta la aplicación:

   ```bash
   py main.py
   ```

## Uso

1. Abre TechInstall.
2. Busca un programa o selecciona una categoría.
3. Marca las aplicaciones que deseas instalar y que tengan un instalador disponible.
4. Pulsa **Instalar seleccionados**.
5. Revisa la ventana de progreso y los resultados.

Los programas que ya están instalados o que no tienen un instalador disponible no se pueden seleccionar.

## Seguridad y licencias

TechInstall es una herramienta de automatización de instalaciones. Los instaladores deben obtenerse de fuentes oficiales y utilizarse respetando sus licencias y condiciones de uso.

La disponibilidad de instalación silenciosa depende del instalador y de los argumentos configurados para cada aplicación.

## Autor

**TeoWebs**

GitHub: [github.com/TeoWebs](https://github.com/TeoWebs)

---

*Proyecto desarrollado con fines prácticos para automatizar tareas habituales de soporte técnico y mantenimiento de equipos Windows.*
