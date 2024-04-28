"""Specific exceptions."""


class HermioneError(Exception):
    """Base exception for my project."""


class UnkownFormat(HermioneError):
    """The object is not build yet."""
