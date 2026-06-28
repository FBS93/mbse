# Activity Model

This package defines the JSON authoring format for activity models and exposes read-only structural queries over validated model data.

## Document shape

An activity model document contains:

- `schema_version`: must be `mbse-activity-model-v0`.
- `document_id`: stable identifier for the model document.
- `initial`: required entry point with one target.
- `actions`: executable steps that call action-language code or another model and continue through one transition.
- `decisions`: boolean conditions with true and false transitions.
- `finals`: terminal points.

## Activity elements

- `initial.target_id`: first action, decision, or final reached by the activity.
- `action.id`, `action.label`: action identity and human-readable label.
- `action.executable`: executable executed by the action.
- `action.transition.target_id`: next action, decision, or final.
- `decision.id`, `decision.label`: decision identity and human-readable label.
- `decision.condition`: executable that resolves the decision branch.
- `decision.true_transition.target_id`: target when the condition returns `true`.
- `decision.false_transition.target_id`: target when the condition returns `false`.
- `final.id`, `final.label`: terminal point identity and human-readable label.

## Executable references

Action executables and decision conditions are declared as either action-language code:

```json
{ "kind": "action_language", "module": "some.module", "name": "some_executable" }
```

or another MBSE model:

```json
{ "kind": "model", "model_id": "some_activity" }
```

- Action executables represent executable activity work.
- Decision conditions must return `true` or `false`.
