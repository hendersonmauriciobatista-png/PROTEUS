"""Desktop bootstrap for the user-owned governed SQLite database."""

import os
from pathlib import Path

from .repository import GovernedCoreRepository


APPLICATION_DIRECTORY_NAME = "Sistema de Monitoramento de Águas"
GOVERNED_DATABASE_NAME = "governed_core_v1.sqlite3"


class DesktopGovernedStartupError(RuntimeError):
    """Typed failure raised when the governed desktop store cannot start."""

    def __init__(self, reason_code, message):
        self.reason_code = reason_code
        super().__init__(message)


def resolve_user_data_root(local_app_data=None):
    """Return the writable per-user application root without using the install tree."""
    root = local_app_data or os.environ.get("LOCALAPPDATA")
    if not root:
        raise DesktopGovernedStartupError(
            "USER_DATA_ROOT_UNRESOLVED",
            "A pasta de dados por usuário não pôde ser resolvida.",
        )
    return Path(root) / APPLICATION_DIRECTORY_NAME / "data"


def initialize_desktop_governed_repository(
    local_app_data=None, migrations_dir=None, repository_factory=GovernedCoreRepository
):
    """Create/open and validate the governed store before the governed UI is shown."""
    try:
        data_root = resolve_user_data_root(local_app_data)
        data_root.mkdir(parents=True, exist_ok=True)
        database_path = data_root / GOVERNED_DATABASE_NAME
        repository = (
            repository_factory(database_path, Path(migrations_dir))
            if migrations_dir is not None
            else repository_factory(database_path)
        )
        repository.initialize()
        return repository
    except DesktopGovernedStartupError:
        raise
    except Exception as error:
        raise DesktopGovernedStartupError(
            "GOVERNED_DATABASE_INITIALIZATION_FAILED",
            "O armazenamento governado não pôde ser inicializado; o fluxo governado foi desabilitado.",
        ) from error
