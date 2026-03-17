#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

HOST = os.getenv("DJANGO_HOST", "127.0.0.1")
PORT = os.getenv("DJANGO_PORT", "8000")

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crowdfunding_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # execute_from_command_line([sys.argv[0], "runserver", f"{HOST}:{PORT}"])
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
