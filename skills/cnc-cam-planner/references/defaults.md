# Default Machining Parameters (Baseline)

Use these as conservative starting points and tune per tool vendor recommendations.

## Radial/Axial Engagement

- Aluminum roughing: 30-45% stepover, up to 0.5xD stepdown
- Steel roughing: 15-30% stepover, up to 0.3xD stepdown
- Finishing: 5-15% stepover, stepdown from scallop target and surface finish requirement

## Clearance and Retracts

- Tool change retract: Z +20 mm from stock top or machine-safe Z
- Linking rapid clearance: Z +5 mm above highest stock feature

## Stock Assumptions

- Default side stock: +2 mm per side
- Default top stock: +1 mm
- Default bottom stock: +0.5 mm for workholding security (if through-cut not required)

## Warnings

- Always dry-run above part before first cut.
- Verify postprocessor against controller dialect (Fanuc, Haas NGC, Siemens, Heidenhain).
