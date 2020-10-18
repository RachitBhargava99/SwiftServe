from fastapi_users.authentication import JWTAuthentication

SECRET = "SECRET-CURRY"

auth_backends = []

jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=10800)

auth_backends.append(jwt_authentication)
