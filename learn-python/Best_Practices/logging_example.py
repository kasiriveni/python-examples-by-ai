"""
Example of using logging for better debugging and monitoring.
"""
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def divide(a, b):
    try:
        result = a / b
        logging.info(f"Division successful: {result}")
        return result
    except ZeroDivisionError as e:
        logging.error("Attempted to divide by zero.")
        raise

if __name__ == "__main__":
    divide(10, 2)
    divide(10, 0)
