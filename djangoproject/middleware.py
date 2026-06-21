from django.conf import settings
from django.http.request import split_domain_port
from django.middleware.locale import LocaleMiddleware
from django.utils.cache import patch_vary_headers
from django.utils.functional import cached_property
from django.utils.http import is_same_domain


class CORSMiddleware:
    """
    Allow only explicitly configured development origins to access responses
    required by the Django Debug Toolbar.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        origin = request.headers.get("Origin")
        allowed_origins = getattr(settings, "CORS_ALLOWED_ORIGINS", ())

        if origin and origin in allowed_origins:
            response["Access-Control-Allow-Origin"] = origin
            patch_vary_headers(response, ("Origin",))

        return response


class ExcludeHostsLocaleMiddleware(LocaleMiddleware):
    """
    Locale middleware that lets us exclude requests to certain hosts (e.g.,
    docs.djangoproject.com) from being processed by LocaleMiddleware.
    """

    @cached_property
    def _excluded_hosts(self):
        return frozenset(getattr(settings, "LOCALE_MIDDLEWARE_EXCLUDED_HOSTS", []))

    def _is_host_included(self, host):
        """
        Mirrors the behavior of django.http.request.validate_host(), but does
        not match '*' (which would exclude all hosts). To exclude all requests
        from being processed by LocaleMiddleware one should simply remove this
        class from settings.MIDDLEWARE.
        """
        domain, _ = split_domain_port(host)
        return not any(
            is_same_domain(domain, pattern) for pattern in self._excluded_hosts
        )

    def process_request(self, request):
        if self._is_host_included(request.get_host()):
            super().process_request(request)

    def process_response(self, request, response):
        if self._is_host_included(request.get_host()):
            return super().process_response(request, response)
        return response
