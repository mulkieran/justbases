"""
Initializations for the tests.
"""
from hypothesis import settings
from hypothesis import HealthCheck

settings.register_profile(
    "tracing", deadline=None, suppress_health_check=[HealthCheck.too_slow])
