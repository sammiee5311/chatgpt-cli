import os
from dotenv import load_dotenv

from utils.log import logger


load_dotenv(dotenv_path=".env")

HOST = os.environ.get("HOST")


def main() -> None:
    logger.info("Completed cookiecutter.")


if __name__ == "__main__":
    main()
