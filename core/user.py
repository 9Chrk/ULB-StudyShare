"""Compatibilité rétroactive: délègue vers auth_service."""

from core.auth_service import add, check

__all__ = ["add", "check"]
