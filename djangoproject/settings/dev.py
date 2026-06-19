from .common import *  # noqa

ALLOWED_HOSTS = [
    "www.djangoproject.localhost",
    "djangoproject.localhost",
    "docs.djangoproject.localhost",
    "dashboard.djangoproject.localhost",
] + SECRETS.get("allowed_hosts", [])

CORS_ALLOWED_ORIGINS = {
    "http://docs.djangoproject.localhost:8000",
}

LOCALE_MIDDLEWARE_EXCLUDED_HOSTS = ["docs.djangoproject.localhost"]

DEBUG = True
THUMBNAIL_DEBUG = DEBUG

# Local development placeholders only.
SECRET_KEY = str(
    SECRETS.get("secret_key") or "development-only-secret-key"
)

SUPERFEEDR_CREDS = SECRETS.get(
    "superfeedr_creds",
    ["developer@example.invalid", "development-placeholder"],
)

STRIPE_SECRET_KEY = SECRETS.get(
    "stripe_secret_key",
    "sk_test_development_placeholder",
)
STRIPE_PUBLISHABLE_KEY = SECRETS.get(
    "stripe_publishable_key",
    "pk_test_development_placeholder",
)
STRIPE_ENDPOINT_SECRET = SECRETS.get(
    "stripe_endpoint_secret",
    "development-webhook-placeholder",
)

PRODUCTS = {
    "monthly": {
        "product_id": SECRETS.get(
            "stripe_product_id_monthly",
            "development_monthly_product",
        ),
        "interval": "month",
        "interval_count": 1,
    },
    "quarterly": {
        "product_id": SECRETS.get(
            "stripe_product_id_quarterly",
            "development_quarterly_product",
        ),
        "interval": "month",
        "interval_count": 3,
    },
    "yearly": {
        "product_id": SECRETS.get(
            "stripe_product_id_yearly",
            "development_yearly_product",
        ),
        "interval": "year",
        "interval_count": 1,
    },
    "onetime": {
        "product_id": SECRETS.get(
            "stripe_product_id_onetime",
            "development_onetime_product",
        ),
        "recurring": False,
    },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        "LOCATION": "trololololol",
    },
    "docs-pages": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        "LOCATION": "docs-pages",
    },
}

CSRF_COOKIE_SECURE = False

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

MEDIA_ROOT = DATA_DIR / "media_root"

SESSION_COOKIE_SECURE = False

STATIC_ROOT = DATA_DIR / "static_root"

# Docs settings
DOCS_BUILD_ROOT = DATA_DIR / "djangodocs"

# django-hosts settings

PARENT_HOST = "djangoproject.localhost:8000"

# django-push settings

PUSH_SSL_CALLBACK = False

# django-debug-toolbar initialization
try:
    import debug_toolbar  # NOQA
except ImportError:
    pass
else:
    INSTALLED_APPS.append("debug_toolbar")
    INTERNAL_IPS = ["127.0.0.1"]
    MIDDLEWARE.insert(
        MIDDLEWARE.index("django.middleware.common.CommonMiddleware") + 1,
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    )
    MIDDLEWARE.insert(
        MIDDLEWARE.index("debug_toolbar.middleware.DebugToolbarMiddleware") + 1,
        "djangoproject.middleware.CORSMiddleware",
    )

# django-recaptcha settings
SILENCED_SYSTEM_CHECKS = SILENCED_SYSTEM_CHECKS + [
    # Default test keys for development.
    "django_recaptcha.recaptcha_test_key_error"
]
