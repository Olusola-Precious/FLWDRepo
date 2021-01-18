#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Eecommerce.settings.development')
    if os.getenv('DJANGO_SETTINGS_MODULE'):
        os.environ['DJANGO_SETTINGS_MODULE'] = os.getenv('DJANGO_SETTINGS_MODULE')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


ENV_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), '.env')
# print("Base = >", ENV_DIR)
load_dotenv(
    ENV_DIR
)
#test_var = os.getenv("APP_NAME")

#print(test_var)


if __name__ == '__main__':
    main()


