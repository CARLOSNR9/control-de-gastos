# Control de Gastos

Este es un proyecto de aplicación web para controlar los gastos, desarrollado con Flask y SQLAlchemy.

## Características

- Registro de transacciones de entrada y salida.
- Filtros por categoría y tipo de transacción.
- Resumen mensual de ingresos y gastos.
- Desglose por categoría.
- Gestión de categorías.

## Requisitos

- Python 3.x
- Flask
- SQLAlchemy
- Flask-SQLAlchemy
- Werkzeug

## Instalación

1. Clona el repositorio:

    ```sh
    git clone https://github.com/CARLOSNR9/control-de-gastos.git
    ```

2. Navega al directorio del proyecto:

    ```sh
    cd control-de-gastos
    ```

3. Crea y activa un entorno virtual:

    - En Windows:
    
        ```sh
        python -m venv venv
        venv\Scripts\activate
        ```

    - En macOS/Linux:

        ```sh
        python3 -m venv venv
        source venv/bin/activate
        ```

4. Instala las dependencias:

    ```sh
    pip install -r requirements.txt
    ```

5. Ejecuta la aplicación:

    ```sh
    python app.py
    ```

## Uso

1. Abre tu navegador web y ve a `http://127.0.0.1:5000`.
2. Utiliza las pestañas para navegar entre la página de registro de transacciones, categorías y reportes.
3. Registra nuevas transacciones, filtra por categoría y tipo, y revisa los reportes mensuales.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue los siguientes pasos para contribuir:

1. Realiza un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-caracteristica`).
3. Realiza los cambios necesarios y realiza commit (`git commit -m 'Agregar nueva característica'`).
4. Empuja los cambios (`git push origin feature/nueva-caracteristica`).
5. Abre un Pull Request.

## Licencia

Este proyecto está licenciado bajo la [MIT License](LICENSE).

