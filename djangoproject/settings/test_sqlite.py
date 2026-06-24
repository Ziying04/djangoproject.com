import sys
from django.db import models

# Mock GeneratedField to be a standard TextField
class DummyGeneratedField(models.TextField):
    def __init__(self, *args, expression=None, output_field=None, db_persist=False, **kwargs):
        super().__init__(*args, **kwargs)

models.GeneratedField = DummyGeneratedField

# Mock SearchVectorField and GinIndex before importing dev settings
import django.contrib.postgres.search
class DummySearchVectorField(models.TextField):
    pass
django.contrib.postgres.search.SearchVectorField = DummySearchVectorField

import django.contrib.postgres.indexes
django.contrib.postgres.indexes.GinIndex = models.Index

from .dev import *

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
    "trac": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "trac.sqlite3",
    },
}

# Remove django_read_only to prevent read-only blocks in SQLite tests
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != "django_read_only"]
