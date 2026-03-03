from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


MaterialType = Literal["aluminum", "steel", "brass", "wood", "plastic"]


@dataclass(frozen=True)
class MaterialSpec:
    name: str
    type: MaterialType
    hardness_hb: int
    chip_load_mm_per_tooth: float
    surface_speed_m_per_min: int


@dataclass(frozen=True)
class MachineSpec:
    name: str
    axis_count: int
    spindle_max_rpm: int
    spindle_power_kw: float
    travel_x_mm: int
    travel_y_mm: int
    travel_z_mm: int
    controller_family: str


@dataclass(frozen=True)
class ToolSpec:
    name: str
    tool_type: Literal["flat_endmill", "ball_endmill", "drill"]
    diameter_mm: float
    flute_count: int
    max_stepdown_mm: float
    max_steover_ratio: float


@dataclass(frozen=True)
class Workpiece:
    x_mm: float
    y_mm: float
    z_mm: float
    material: MaterialType


@dataclass(frozen=True)
class PlanRequest:
    part_name: str
    mesh_bounds_mm: tuple[float, float, float]
    tolerance_mm: float
    stock_allowance_mm: float
    material: MaterialType


@dataclass(frozen=True)
class PlanResult:
    machine: MachineSpec
    roughing_tool: ToolSpec
    finishing_tool: ToolSpec
    spindle_rpm: int
    feed_mm_min: float
    stepdown_mm: float
    stepover_mm: float
    mcode_program: str
    gcode_program: str
