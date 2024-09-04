Project: AgenAICodex
=================

## Configuración

Antes de ejecutar la aplicación, asegúrate de configurar las siguientes variables de entorno:

file: `.env`

```bash
    OPENAI_API_KEY=
    LANGCHAIN_API_KEY=
```

## Ejecución

Para ejecutar la aplicación, simplemente usa el siguiente comando:

```bash
streamlit run main.py
```

Namespace AgenAICodex
=====================

Sub-modules
-----------
* AgenAICodex.main
* AgenAICodex.model


Module AgenAICodex.main
=======================

Functions
---------

`main()`
:   Punto de entrada principal para la ejecución del programa.
    Este bloque se ejecuta solo si el script se ejecuta directamente.
    Crea una instancia de la clase App y llama al método run para iniciar la aplicación.


Module AgenAICodex.model.app
============================

Classes
-------

`App()`
:   Clase que representa la aplicación de un agente de inteligencia artificial
    diseñado para responder preguntas sobre programación utilizando código Python.

    Inicializa la aplicación cargando la configuración y definiendo el archivo
    donde se guardará el historial de interacciones.

    Attributes:
        config (dict): Configuración cargada desde el archivo de configuración.
        historyFile (str): Nombre del archivo que almacena el historial de preguntas y respuestas.

    ### Methods

    `agen_run(self, agent_executor, user_input)`
    :   Ejecuta el agente con la entrada del usuario, muestra la respuesta y guarda
        la interacción en el historial.

        Args:
            agent_executor (AgentExecutor): El ejecutor del agente que procesa la entrada.
            user_input (str): La entrada proporcionada por el usuario.

    `clear_history(self)`
    :   Limpia el historial de preguntas y respuestas, vaciando el archivo correspondiente.

    `download_file(self)`
    :   Lee el contenido del archivo de historial y lo devuelve.

        Returns:
            str: Contenido del archivo de historial.

    `load_history(self)`
    :   Carga el historial de preguntas y respuestas desde el archivo.

        Returns:
            list: Una lista de las líneas del historial. Si el archivo no existe,
            devuelve una lista vacía.

    `run(self)`
    :   Configura y ejecuta la interfaz de usuario de la aplicación utilizando Streamlit.
        Carga el prompt del agente, configura los botones y maneja las interacciones del usuario.

    `save_history(self, question, answer)`
    :   Guarda una pregunta y su respuesta en el historial.

        Args:
            question (str): La pregunta realizada al agente.
            answer (str): La respuesta proporcionada por el agente.


Module AgenAICodex.model.config
===============================

Classes
-------

`Config()`
:   Clase para manejar la configuración cargada desde un archivo JSON.

    Esta clase permite cargar y acceder a los valores de configuración
    almacenados en un archivo, facilitando la gestión de parámetros
    necesarios para el funcionamiento de la aplicación.

    ### Static methods

    `get_all(filepath='model/config-model.json')`
    :   Carga y devuelve todos los valores del archivo de configuración.

        Si la configuración ya ha sido cargada, simplemente se devuelve
        el contenido almacenado en memoria. De lo contrario, se carga
        desde el archivo especificado y se almacena para futuros accesos.

        Args:
            filepath (str): Ruta al archivo JSON que contiene la configuración.
                             Por defecto, se utiliza "model/config-model.json".

        Returns:
            dict: Un diccionario con todos los valores de configuración
                  cargados desde el archivo JSON.
