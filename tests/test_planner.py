from cnc_simulator import CncPlanner
from cnc_simulator.models import PlanRequest


def test_plan_selects_machine_and_generates_code():
    planner = CncPlanner()
    plan = planner.create_plan(
        PlanRequest(
            part_name="demo_part",
            mesh_bounds_mm=(100, 80, 30),
            tolerance_mm=0.2,
            stock_allowance_mm=1.0,
            material="aluminum",
        )
    )

    assert plan.machine.name
    assert "M6" in plan.mcode_program
    assert "G21 G17 G90" in plan.gcode_program


def test_raises_when_part_exceeds_machine_travel():
    planner = CncPlanner()
    try:
        planner.create_plan(
            PlanRequest(
                part_name="too_large",
                mesh_bounds_mm=(5000, 5000, 1000),
                tolerance_mm=0.5,
                stock_allowance_mm=2.0,
                material="steel",
            )
        )
    except ValueError as exc:
        assert "No machine" in str(exc)
    else:
        raise AssertionError("Expected ValueError for oversized part")
