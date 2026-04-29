"""Example runner for Module 9: Production AI Apps (logging demo)"""
import logging


def main():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("module9_example")
    logger.info("Module 9 - Production example starting")
    for i in range(3):
        logger.info("Processing item %d", i)
    logger.info("Done")


if __name__ == "__main__":
    main()
