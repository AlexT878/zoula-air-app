class ErrorCode:
    EMAIL_ALREADY_EXISTS = "EMAIL_ALREADY_EXISTS"
    EMAIL_ALREADY_EXISTS_MESSAGE = "A user with this email already exists."
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    INCORRECT_LOGIN = "Incorrect email or password"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    USER_NOT_FOUND_INACTIVE_MESSAGE = "User not found or inactive"
    USER_NOT_FOUND_MESSAGE = "User not found in database"
    INACTIVE_USER = "Inactive user"

    TOKEN_INVALID = "Invalid token"
    TOKEN_MISSING_SUBJECT = "Token is missing subject (user ID)"
    TOKEN_EXPIRED = "Token has expired"
    TOKEN_INVALID_CREDENTIALS = "Could not validate credentials"
    TOKEN_INVALID_TYPE = "Invalid token type"
    TOKEN_NO_ROLES = "Missing required roles"

    PASSWORD_TOO_SHORT = "Password must be at least 8 characters long."
    PASSWORD_NO_UPPER = "Password must contain at least one uppercase letter."
    PASSWORD_NO_LOWER = "Password must contain at least one lowercase letter."
    PASSWORD_NO_DIGIT = "Password must contain at least one digit."
    PASSWORD_NO_SPECIAL = (
        "Password must contain at least one special character (@$!%*?&)."
    )
