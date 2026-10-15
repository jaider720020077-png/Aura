# Aura Centro de Bienestar

Sitio de Aura para Streamlit, con portada pública adaptable a celular y computador, servicios, galería, mapa, solicitudes de cita y panel privado de administración.

## Ejecutar en tu computador

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Publicar en Streamlit Community Cloud

1. Sube esta carpeta completa a un repositorio de GitHub.
2. Entra a https://share.streamlit.io/ e inicia sesión con GitHub.
3. Elige **Create app**, selecciona el repositorio y como archivo principal escribe `streamlit_app.py`.
4. Pulsa **Deploy**.

## Importante

El archivo de inicio es `streamlit_app.py`. En el panel de demostración entra con `aura2026`.

Esta versión es una demostración: los cambios, imágenes y reservas viven durante la sesión actual de Streamlit. Antes de usarla con clientes reales, hay que conectar una base de datos y almacenamiento de imágenes para que la información se conserve y se comparta entre dispositivos, y reemplazar la contraseña temporal por autenticación real.
