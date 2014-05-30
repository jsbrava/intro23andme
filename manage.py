#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "intro.settings")
    # trying this hack because of error with postgres and import psycopg2
    os.environ['DYLD_LIBRARY_PATH'] = '/Library/PostgreSQL/9.3/lib'
    
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
