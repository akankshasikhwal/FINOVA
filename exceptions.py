# exceptions.py
# Custom exceptions for SmartSpend.


class ValidationError(ValueError):
    """Raised when user-supplied data fails a business-rule check.

    Inherits from ValueError so callers can catch either type.
    The message should always be human-readable (shown directly in the UI).
    """
