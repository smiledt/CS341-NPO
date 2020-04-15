# A Python script file to generate generic events for the book_keeping app
from faker import Faker
from book_keeping.models import Event
import random
import django
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CS341_NPO.settings')

django.setup()

# FAKE POP SCRIPT

# Instantiate it
fakegen = Faker()
