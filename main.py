from model.app import App


def main():
    """
    Punto de entrada principal para la ejecución del programa.
    Este bloque se ejecuta solo si el script se ejecuta directamente.
    Crea una instancia de la clase App y llama al método run para iniciar la aplicación.
    """
    app = App()
    app.run()


if __name__ == "__main__":
    main()
