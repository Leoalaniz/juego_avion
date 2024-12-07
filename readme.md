
# Mi Juego

Este es un proyecto de juego básico escrito en Python, organizado en paquetes para una mejor estructura y escalabilidad. Incluye una interfaz gráfica simple, lógica del juego y utilidades generales.

## Estructura del Proyecto

```
mi_juego/
├── src/
│    ├── core/            # Lógica central del juego
│    ├── gui/             # Interfaz gráfica del usuario
│    ├── utils/           # Utilidades generales
│    └── main.py          # Punto de entrada del juego
├── test/                 # Pruebas unitarias
├── assets/               # Recursos (imágenes, sonidos, etc.)
├── venv/                 # Entorno virtual
├── juego.db              # Base de datos del juego
└── .gitignore            # Archivos ignorados por Git
```

## Requisitos Previos

- Python 3.8 o superior.
- Virtualenv o cualquier herramienta de entornos virtuales.

## Instalación

1. Clona este repositorio:
   ```bash
   git clone <URL-del-repositorio>
   cd mi_juego
   ```

2. Crea y activa un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate   # En Linux/Mac
   venv\Scripts\activate      # En Windows
   ```

3. Instala las dependencias (si las hay):
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Ejecuta el juego desde el archivo principal:
   ```bash
   python src/main.py
   ```

2. Sigue las instrucciones en la consola o interfaz gráfica.

## Pruebas

El proyecto incluye pruebas unitarias para los módulos en `src/core`. Para ejecutarlas:

```bash
python -m unittest discover -s test
```

## Contribución

Si deseas contribuir, sigue estos pasos:

1. Haz un fork de este repositorio.
2. Crea una nueva rama para tus cambios:
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```
3. Realiza tus cambios y sube los commits.
4. Envía un Pull Request.

## Licencia

Este proyecto está bajo la [Licencia MIT](Leo_Alaniz).

---

¡Gracias por probar **Mi Juego**! Si tienes ideas o encuentras errores, no dudes en abrir un issue.
