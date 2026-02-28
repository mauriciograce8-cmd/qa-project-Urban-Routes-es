# Proyecto Urban Routes: Automatización de Pruebas E2E

## Descripción del Proyecto
El proyecto consiste en la creación de caso de pruebas automatizadas para la aplicación de servicios de taxi "Urban Routes". El objetivo es validar el flujo completo de reservación, asegurando que un usuario pueda ingresar direcciones, seleccionar tarifas específicas (Comfort), vincular métodos de pago, validar su identidad mediante SMS y añadir requisitos especiales para su viaje.

## Tecnologías y Técnicas Utilizadas
Para comprobar que las pruebas funcionaron, se aplicaron:
*   **Lenguaje:** Python 3.14
*   **Herramienta de Automatización:** Selenium WebDriver.
*   **Patrón de Diseño:** Page Object Model (POM), organizando selectores y métodos.
*   **Manejo de Esperas:** Uso de esperas explícitas (`WebDriverWait`) para sincronizar el código con la carga de elementos.
*   **Interacción Avanzada:** Uso de `JavaScript Executor` para realizar clics en botones que presentan bloqueos visuales y simulación de teclado (`Keys.TAB`) para validación de formularios.
*   **Pruebas de Red:** Intercepción de logs de rendimiento del navegador para recuperar códigos de confirmación SMS de forma automática.

## Instrucciones para Ejecutar las Pruebas
Estos son los pasos para correr los tests en un entorno local:

1.  **Requisitos:** Asegúrarse de tener instalado Python y las bibliotecas necesarias:
    ```bash
    pip install selenium
    ```
2.  **Configuración de Datos:** Abre el archivo `data.py` y actualiza la variable `urban_routes_url` con una URL de servidor activa.
3.  **Ejecución:** 
    *   Desde PyCharm: Haz clic derecho en `main.py` y selecciona **Run 'main'**.
    *   Desde la terminal: Ejecuta el comando `pytest main.py`.
Use code with caution.