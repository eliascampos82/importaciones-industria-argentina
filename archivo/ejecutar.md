# Ejecutar el proyecto

Abrir la carpeta `PROYECTO DATOS` en VS Code → `Terminal` → `New Terminal`.

## La primera vez

1. Crear el entorno:
   ```
   python -m venv .venv
   ```
2. Instalar lo necesario:
   ```
   .\.venv\Scripts\python.exe -m pip install -r requirements.txt
   ```
3. Ejecutar:
   ```
   .\.venv\Scripts\python.exe -m streamlit run dashboard/Inicio.py
   ```
4. Abrir en el navegador: <http://localhost:8501>

## Las siguientes veces

1. Ejecutar:
   ```
   .\.venv\Scripts\python.exe -m streamlit run dashboard/Inicio.py
   ```
2. Abrir en el navegador: <http://localhost:8501>

Para cerrar: `Ctrl + C` en la terminal.
