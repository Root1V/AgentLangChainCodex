import json


class Config:
    """
    Clase para manejar la configuración cargada desde un archivo JSON.

    Esta clase permite cargar y acceder a los valores de configuración
    almacenados en un archivo, facilitando la gestión de parámetros
    necesarios para el funcionamiento de la aplicación.
    """

    _config = None

    @classmethod
    def get_all(cls, filepath="model/config-model.json"):
        """Carga y devuelve todos los valores del archivo de configuración.

        Si la configuración ya ha sido cargada, simplemente se devuelve
        el contenido almacenado en memoria. De lo contrario, se carga
        desde el archivo especificado y se almacena para futuros accesos.

        Args:
            filepath (str): Ruta al archivo JSON que contiene la configuración.
                             Por defecto, se utiliza "model/config-model.json".

        Returns:
            dict: Un diccionario con todos los valores de configuración
                  cargados desde el archivo JSON.
        """
        if cls._config is None:
            with open(filepath, "r") as f:
                cls._config = json.load(f)
        return cls._config
