from __future__ import annotations

from typing import Protocol


class HasStoredInPrivateFlag(Protocol):
    @property
    def stored_in_private(self) -> bool: ...
