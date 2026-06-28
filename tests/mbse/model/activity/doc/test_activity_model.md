# Activity Model Test

This test file validates the shared activity model fixture as authored data.

- Confirms the JSON fixture loads and validates against the activity schema.
- Confirms structural queries return the expected initial entry point, actions, decisions, and finals.
- Confirms unknown action, decision, and final lookups fail explicitly instead of returning ambiguous results.
