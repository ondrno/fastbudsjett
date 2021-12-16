# Statement for enabling the development environment
DEBUG = True

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED = True

# Use a secure, unique and absolutely secret key for
# signing the data.
CSRF_SESSION_KEY = "DO3TQLDL1V5R04SIMJ3QWMVA0UZV5H9OB27RDRJLSE2Y9061PFHBR3RX3HJF4IT6"

# Secret key for signing cookies
SECRET_KEY = "CAA6F5A90986C52E2355403D227D3F68880C8B107ABF06AE4A5331B64C666B9F"
