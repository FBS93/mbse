# HSM Model

This package defines the JSON authoring format for hierarchical state machine models and provides read-only queries over validated model data.

## Document shape

An HSM model document contains:

- `schema_version`: must be `mbse-hsm-model-v0`.
- `document_id`: stable identifier for the model document.
- `events`: handled event declarations and optional typed parameters.
- `initial_transition`: required root initial target.
- `states`: top-level states, each of which may contain nested states.

## Typed values

Event parameters use the shared typed declaration model.

- `signed`, `unsigned`, and `float` declare mandatory `min` and `max` bounds.
- `bool` carries no extra attributes.
- `enum` references one global enum by `enum_id`.

Enum parameters reference shared context enums by `enum_id`.

## State elements

Each state defines a subset of these elements:

- `id`, `label`: state identity and human-readable label.
- `states`: child states for hierarchical decomposition.
- `hooks.on_entry`: activities executed when the state is entered.
- `hooks.on_exit`: activities executed when the state is exited.
- `initial_transition`: required only when the state has its own local default child path.
- `internal_transitions`: event handlers that consume an event without changing active state.
- `external_transitions`: event handlers that change state.

## Transition elements

- `initial_transition.target_id`: target state entered automatically.
- `initial_transition.activities`: activities executed on that initial transition before entering its target path.
- `internal_transition.event_id`: event consumed in place.
- `internal_transition.activities`: activities executed for that internal transition.
- `external_transition.event_id`: triggering event.
- `external_transition.target_id`: direct target for an unguarded transition.
- `external_transition.activities`: activities executed after exits and before new entries.
- `external_transition.guard_condition`: alternative to `target_id`; contains one `guard_activity` plus `true_branch` and `false_branch` targets with optional branch-specific activities.

## Executable references

Hooks, activities, and guards are declared as:

```json
{ "kind": "action_language", "module": "some.module", "name": "some_executable" }
```

- Hook and activity executables may mutate runtime variables.
- Guard executables must return `true` or `false`.

## Representative example

```json
{
  "schema_version": "mbse-hsm-model-v0",
  "document_id": "door_controller",
  "events": [
    { "id": "unlock", "label": "Unlock" },
    { "id": "open", "label": "Open" }
  ],
  "initial_transition": { "target_id": "closed" },
  "states": [
    {
      "id": "closed",
      "label": "Closed",
      "hooks": {
        "on_entry": [
          { "kind": "action_language", "module": "app.hsm_actions", "name": "closed_entry" }
        ]
      },
      "external_transitions": [
        {
          "event_id": "unlock",
          "guard_condition": {
            "guard_activity": {
              "kind": "action_language",
              "module": "app.hsm_actions",
              "name": "can_unlock"
            },
            "true_branch": {
              "target_id": "closed",
              "activities": [
                { "kind": "action_language", "module": "app.hsm_actions", "name": "unlock_action" }
              ]
            },
            "false_branch": {
              "target_id": "closed"
            }
          }
        },
        {
          "event_id": "open",
          "target_id": "opened",
          "activities": [
            { "kind": "action_language", "module": "app.hsm_actions", "name": "open_action" }
          ]
        }
      ]
    },
    {
      "id": "opened",
      "label": "Opened"
    }
  ]
}
```
