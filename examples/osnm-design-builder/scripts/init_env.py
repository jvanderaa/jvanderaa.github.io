"""Create fresh, private credentials for this isolated loopback lab."""
from pathlib import Path
import secrets

root = Path(__file__).resolve().parent.parent
p = root / '.lab.env'
if p.exists():
    print('Existing .lab.env retained.')
else:
    db = secrets.token_urlsafe(24)
    values = {
        'NAUTOBOT_ALLOWED_HOSTS': 'localhost 127.0.0.1',
        'NAUTOBOT_DB_HOST': 'db', 'NAUTOBOT_DB_NAME': 'nautobot', 'NAUTOBOT_DB_USER': 'nautobot',
        'NAUTOBOT_DB_PASSWORD': db, 'POSTGRES_DB': 'nautobot', 'POSTGRES_USER': 'nautobot', 'POSTGRES_PASSWORD': db,
        'NAUTOBOT_REDIS_HOST': 'redis', 'NAUTOBOT_REDIS_PORT': '6379',
        'NAUTOBOT_SECRET_KEY': secrets.token_urlsafe(64),
        'NAUTOBOT_CREATE_SUPERUSER': 'true', 'NAUTOBOT_SUPERUSER_NAME': 'blog-admin',
        'NAUTOBOT_SUPERUSER_EMAIL': 'blog-admin@example.invalid',
        'NAUTOBOT_SUPERUSER_PASSWORD': secrets.token_urlsafe(24),
        'NAUTOBOT_SUPERUSER_API_TOKEN': secrets.token_hex(20),
        'NAUTOBOT_DEBUG': 'false', 'NAUTOBOT_LOG_LEVEL': 'INFO',
        'NAUTOBOT_CONFIG': '/opt/nautobot/nautobot_config.py',
    }
    p.write_text(''.join(f'{k}={v}\n' for k,v in values.items()))
    p.chmod(0o600)
    print('Created .lab.env (0600). Credentials are not displayed.')
