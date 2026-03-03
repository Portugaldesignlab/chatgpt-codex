from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import MachineSpec, MaterialSpec, ToolSpec


CATALOG_DIR = Path(__file__).parent / "catalogs"


def _load_json(filename: str) -> list[dict[str, Any]]:
    return json.loads((CATALOG_DIR / filename).read_text())


def load_materials() -> list[MaterialSpec]:
    return [MaterialSpec(**row) for row in _load_json("materials.json")]


def load_machines() -> list[MachineSpec]:
    return [MachineSpec(**row) for row in _load_json("machines.json")]


def load_tools() -> list[ToolSpec]:
    return [ToolSpec(**row) for row in _load_json("tools.json")]
