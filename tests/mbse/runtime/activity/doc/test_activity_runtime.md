# Activity Runtime Tests

These tests cover the observable behavior of `ActivityRuntime` using the reference activity and shared context fixtures.

- initialization starts paused and plans the initial target
- `play()` drains true and false paths to a final node
- action executables can mutate declared runtime variables
- decision conditions must return `bool`
- `step()` exposes pending execution one runtime step at a time
- `pending_decision` contains both precalculated branches before execution
- the execution log records the expected activity sequence
