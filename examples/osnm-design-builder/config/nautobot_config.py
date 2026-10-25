"""Isolated OSNM screenshot lab; no external systems or production data."""
from nautobot.core.settings import *  # noqa: F403

PLUGINS = ['nautobot_design_builder']
PLUGINS_CONFIG = {'nautobot_design_builder': {}}
BANNER_TOP = 'OSNM DESIGN LAB · Synthetic inventory · Model changes only'
BANNER_BOTTOM = 'Blog demonstration · No network devices are configured'
BANNER_LOGIN = 'Local isolated screenshot lab'
JOBS_ROOT = '/opt/nautobot/jobs'
TIME_ZONE = 'America/Chicago'
INSTALLATION_METRICS_ENABLED = False
