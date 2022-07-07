import enum


class TokenType(enum.Enum):
    access = "access"
    refresh = "refresh"


class FigureType(str, enum.Enum):
    map = "multiline"
