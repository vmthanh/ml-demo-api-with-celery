# Gunicorn configurations:
# http://docs.gunicorn.org/en/stable/settings.html

workers = 4  # Number of Uvicorn proceses are generated by 1 Gunicorn process
# Gunicorn would act as a process manager, listening on the port and the IP.
# And it would transmit the communication to the worker processes running the Uvicorn class.
worker_class = "uvicorn.workers.UvicornWorker"
