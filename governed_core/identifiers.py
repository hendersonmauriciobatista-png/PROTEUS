"""Non-semantic, system-assigned identifiers for governed Core V1."""

from uuid import uuid4


class IdentifierFactory:
    PREFIXES = {
        "point": "pnt",
        "context_revision": "ctx",
        "aps": "aps",
        "basis": "bas",
        "event": "gev",
        "authority": "aut",
        "evidence": "evi",
        "measurement": "mea",
        "evaluation": "eva",
        "aps_applicability": "apa",
    }

    def new(self, kind):
        try:
            prefix = self.PREFIXES[kind]
        except KeyError as error:
            raise ValueError(f"Tipo de identificador desconhecido: {kind}") from error
        return f"{prefix}_{uuid4().hex}"

    def validate(self, kind, value):
        prefix = self.PREFIXES.get(kind)
        if prefix is None:
            raise ValueError(f"Tipo de identificador desconhecido: {kind}")
        expected_prefix = f"{prefix}_"
        suffix = value[len(expected_prefix):] if isinstance(value, str) and value.startswith(expected_prefix) else ""
        if len(suffix) != 32 or any(character not in "0123456789abcdef" for character in suffix):
            raise ValueError(f"Identificador {kind} invalido: {value}")
        return True
