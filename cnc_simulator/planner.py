from __future__ import annotations

from math import floor, pi

from .catalog import load_machines, load_materials, load_tools
from .models import MachineSpec, PlanRequest, PlanResult, ToolSpec


class CncPlanner:
    """Select machine/tooling and emit starter M/G code from a part envelope."""

    def create_plan(self, request: PlanRequest) -> PlanResult:
        machine = self._pick_machine(request)
        roughing_tool, finishing_tool = self._pick_tools(request)
        material = next(m for m in load_materials() if m.type == request.material)

        spindle_rpm = min(
            floor((material.surface_speed_m_per_min * 1000) / (pi * roughing_tool.diameter_mm)),
            machine.spindle_max_rpm,
        )
        feed_mm_min = spindle_rpm * roughing_tool.flute_count * material.chip_load_mm_per_tooth
        stepdown_mm = min(roughing_tool.max_stepdown_mm, request.mesh_bounds_mm[2] / 10)
        stepover_mm = roughing_tool.diameter_mm * roughing_tool.max_steover_ratio

        mcode = self._render_m_code(machine)
        gcode = self._render_g_code(request, roughing_tool, finishing_tool, spindle_rpm, feed_mm_min, stepdown_mm, stepover_mm)

        return PlanResult(
            machine=machine,
            roughing_tool=roughing_tool,
            finishing_tool=finishing_tool,
            spindle_rpm=spindle_rpm,
            feed_mm_min=round(feed_mm_min, 2),
            stepdown_mm=round(stepdown_mm, 2),
            stepover_mm=round(stepover_mm, 2),
            mcode_program=mcode,
            gcode_program=gcode,
        )

    def _pick_machine(self, request: PlanRequest) -> MachineSpec:
        x, y, z = request.mesh_bounds_mm
        for machine in load_machines():
            if machine.travel_x_mm >= x and machine.travel_y_mm >= y and machine.travel_z_mm >= z:
                return machine
        raise ValueError("No machine in catalog has enough travel for the part envelope")

    def _pick_tools(self, request: PlanRequest) -> tuple[ToolSpec, ToolSpec]:
        tools = load_tools()
        roughing = next(t for t in tools if t.tool_type == "flat_endmill" and t.diameter_mm >= max(6.0, request.stock_allowance_mm * 6))
        finishing = next(t for t in tools if t.tool_type == "ball_endmill" and t.diameter_mm <= max(6.0, request.tolerance_mm * 20))
        return roughing, finishing

    def _render_m_code(self, machine: MachineSpec) -> str:
        return "\n".join(
            [
                f"(Controller: {machine.controller_family})",
                "M6 (tool change)",
                "M3 (spindle clockwise)",
                "M8 (coolant on)",
                "M30 (program end and reset)",
            ]
        )

    def _render_g_code(
        self,
        request: PlanRequest,
        roughing_tool: ToolSpec,
        finishing_tool: ToolSpec,
        spindle_rpm: int,
        feed_mm_min: float,
        stepdown_mm: float,
        stepover_mm: float,
    ) -> str:
        x, y, z = request.mesh_bounds_mm
        return "\n".join(
            [
                f"(PART {request.part_name})",
                "G21 G17 G90",
                f"T1 M6 ({roughing_tool.name})",
                f"S{spindle_rpm} M3",
                f"F{round(feed_mm_min, 1)}",
                "G0 Z10.0",
                "G0 X0 Y0",
                f"(Roughing: stepdown={round(stepdown_mm, 2)} stepover={round(stepover_mm, 2)})",
                f"G1 Z-{round(z - request.stock_allowance_mm, 2)}",
                f"G1 X{round(x, 2)} Y0",
                f"G1 X{round(x, 2)} Y{round(y, 2)}",
                f"G1 X0 Y{round(y, 2)}",
                "G1 X0 Y0",
                f"T2 M6 ({finishing_tool.name})",
                f"F{round(feed_mm_min * 0.6, 1)}",
                "(Finishing pass placeholder: integrate mesh-slicing strategy here)",
                "G0 Z15.0",
                "M5",
                "M9",
                "M30",
            ]
        )
