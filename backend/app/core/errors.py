class ErrorCode:
    EMAIL_ALREADY_EXISTS = "EMAIL_ALREADY_EXISTS"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"

    PASSWORD_TOO_SHORT = "Password must be at least 8 characters long."
    PASSWORD_NO_UPPER = "Password must contain at least one uppercase letter."
    PASSWORD_NO_LOWER = "Password must contain at least one lowercase letter."
    PASSWORD_NO_DIGIT = "Password must contain at least one digit."
    PASSWORD_NO_SPECIAL = (
        "Password must contain at least one special character (@$!%*?&)."
    )
