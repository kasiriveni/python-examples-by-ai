# Sentry: Error Tracking

import sentry_sdk

# Initialize Sentry
sentry_sdk.init(
    dsn="<your_sentry_dsn>",
    traces_sample_rate=1.0
)

# Example function with an error
def divide(a, b):
    return a / b

try:
    divide(1, 0)
except ZeroDivisionError as e:
    sentry_sdk.capture_exception(e)
    print("Error captured by Sentry")
