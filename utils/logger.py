import logging

class Logger:
    def __init__(self, log_file='log.txt', level=logging.DEBUG):
        self.log_file = log_file
        self.level = level
        self.logger = self._create_logger()

    def _create_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(self.level)

        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(self.level)
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

# Exemplo de uso:
if __name__ == "__main__":
    logger = Logger()
    logger.debug("Mensagem de debug")
    logger.info("Mensagem de informação")
    logger.warning("Mensagem de aviso")
    logger.error("Mensagem de erro")
    logger.critical("Mensagem crítica")
