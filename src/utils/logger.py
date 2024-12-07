import logging

# Configuración básica del logger
def setup_logger():
    # Establecer el formato del log
    log_format = '%(asctime)s - %(levelname)s - %(message)s'
    logging.basicConfig(filename='juego.log', level=logging.DEBUG, format=log_format)
    logging.info("Logger configurado correctamente")

# Función para obtener el logger
def get_logger():
    return logging.getLogger()
