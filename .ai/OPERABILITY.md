# Operability

Current estimate: **28%**

- Development usable: PASS
- Internal testing ready: PASS
- External beta/testing ready: FAIL
- Real external-audience representative output: FAIL
- Production ready: FAIL
- Publishable Episode 1: FAIL

## External testing gate
Requires approved canonical character + atomic props/backgrounds + passing 15s benchmark + clean rerun + no blocking P0/P1 defect.

## External-audience gate
Requires external-testing gate + passing 45s cold open + stable branding/timing/factual QC + reproducibility.

## Production gate
Requires full Episode 1 source-to-final build, sync verification, restart/recovery, useful logs, final QC, and acceptable blocker state.

Never call the project ready unless the relevant gate actually passes.
