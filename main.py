
import sys
import os

sys.path.insert(1, './')

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "_configs.settings")
    os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
    import django
    django.setup()


BASE_DIR = os.path.dirname(__file__)

if __name__ == "__main__":

    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))

    HOST = f'{s.getsockname()[0]}:80'

    os.system(f"python {os.path.join(BASE_DIR, 'manage.py')} runserver {HOST}")

