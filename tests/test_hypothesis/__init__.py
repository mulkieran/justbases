"""
Initializations for the tests.
"""

from hypothesis import HealthCheck, settings

settings.register_profile(
    "tracing", deadline=None, suppress_health_check=[HealthCheck.too_slow]
)
