---
name: cnc-cam-planner
description: Build CNC milling simulation and CAM planning workflows with realistic machine, tooling, and material constraints; use when generating machining plans from uploaded 3D models, selecting stock material, choosing available market machines/tools, and producing safe starter M-code and G-code.
---

# CNC CAM Planner Skill

## Workflow

1. Parse uploaded model metadata and extract envelope dimensions, minimum feature radius, and target tolerance.
2. Validate stock setup by matching user-selected material against machine envelope and fixture allowance.
3. Choose machine from the supported catalog by axis count, travel limits, spindle speed range, and control family.
4. Choose roughing and finishing tools from catalog with diameter, flute count, and recommended axial/radial engagement.
5. Compute baseline parameters:
   - spindle rpm from cutting speed and tool diameter
   - feed rate from chip load × flute count × rpm
   - roughing stepdown and stepover from tool and material limits
6. Emit operation sequence: facing (optional), roughing, rest machining (optional), finishing, drilling (optional).
7. Output starter M-code/G-code plus validation notes and simulation warnings.

## Safety Rules

- Reject plans when part envelope exceeds machine travel.
- Add retract and clearance moves before tool changes.
- Use lower feed override defaults for steel and unknown alloys.
- Flag collision risk when holder clearance is unknown.
- Mark generated code as "starter code requiring machine-side verification".

## Output Contract

Return:

- selected machine and why
- selected tools and why
- material and stock assumptions
- cutting parameters table
- M-code block
- G-code block
- simulation and operator warnings

Load numeric defaults from `references/defaults.md` and machine/material priors from `references/market-catalog-notes.md`.
