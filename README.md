# CNC Simulator + CAM Planner (Starter)

This repository now includes a **starter backend core** for a CNC milling simulator/planner that:

- Accepts 3D-part envelope inputs (from uploaded model analysis stage)
- Selects realistic market machine/tool/material data from catalogs
- Computes conservative first-pass cutting parameters
- Emits starter **M-code** and **G-code** blocks

## Why this is useful

Your request needs real-world grounding (actual machine/tool families, material-aware parameters, and safety checks). This starter gives you a solid base to build a full product UI and mesh-analysis pipeline on top.

## Included components

- `cnc_simulator/models.py` — strongly-typed planning models
- `cnc_simulator/catalog.py` — loader for machine/tool/material catalogs
- `cnc_simulator/planner.py` — planning engine and code generation
- `cnc_simulator/catalogs/*.json` — market-inspired defaults
- `skills/cnc-cam-planner/*` — reusable Codex skill for structured CNC planning

## Quick usage

```python
from cnc_simulator import CncPlanner
from cnc_simulator.models import PlanRequest

planner = CncPlanner()
plan = planner.create_plan(
    PlanRequest(
        part_name="impeller_demo",
        mesh_bounds_mm=(120, 80, 35),
        tolerance_mm=0.2,
        stock_allowance_mm=1.0,
        material="aluminum",
    )
)

print(plan.machine.name)
print(plan.roughing_tool.name)
print(plan.gcode_program)
```

## Next steps toward full product

1. Add mesh analysis stage (STL/STEP parser + feature extraction).
2. Add strategy generator (adaptive roughing, rest milling, scallop finishing).
3. Add geometric simulation and collision checks (tool + holder + fixture).
4. Add postprocessor layer per controller dialect.
5. Build frontend upload/simulation UI.

> Important: generated NC output is **starter code** and must be verified in machine simulation and at the controller before production.
