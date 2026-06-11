from mbse.runtime.hsm.runtime_model.runtime_model_types import HsmGeneratedRuntimeCallablePlan
from mbse.runtime.hsm.runtime_model.runtime_model_types import HsmGeneratedRuntimeEventCandidateRow
from mbse.runtime.hsm.runtime_model.runtime_model_types import HsmGeneratedRuntimeGuardBranchRow
PARENTS = {"idle": None, "idle_waiting": "idle", "open": None}

ANCESTRY_BY_STATE = {"idle": ("idle",), "idle_waiting": ("idle", "idle_waiting"), "open": ("open",)}

INITIAL_TARGETS = {None: "idle", "idle": "idle_waiting"}

INITIAL_TRANSITION_IDS = {None: "machine_init", "idle": "idle_init"}

CALLABLE_PLANS_BY_ID = {}

ON_INITIAL_PLAN_IDS_BY_STATE = {"idle": (), "idle_waiting": (), "open": ()}

ON_ENTRY_PLAN_IDS_BY_STATE = {"idle": (), "idle_waiting": (), "open": ()}

ON_EXIT_PLAN_IDS_BY_STATE = {"idle": (), "idle_waiting": (), "open": ()}

EVENT_CANDIDATE_ROWS_BY_STATE = {"idle": (HsmGeneratedRuntimeEventCandidateRow(candidate_id="idle_pulse", event_id="pulse_evt", source_id="idle", kind="internal", activity_plan_ids=()),), "idle_waiting": (HsmGeneratedRuntimeEventCandidateRow(candidate_id="waiting_to_open", event_id="open_evt", source_id="idle_waiting", kind="external_transition", target_id="open", activity_plan_ids=()),), "open": (HsmGeneratedRuntimeEventCandidateRow(candidate_id="open_to_idle", event_id="close_evt", source_id="open", kind="external_transition", target_id="idle", activity_plan_ids=()),)}

LEAF_STATES = frozenset({"idle_waiting", "open"})

def state_idle(ctx, event_id):
  return ("unhandled", None)

def state_idle_waiting(ctx, event_id):
  if event_id == "open_evt":
    return ("external_transition", "open")
  return ("unhandled", None)

def state_open(ctx, event_id):
  if event_id == "close_evt":
    return ("external_transition", "idle")
  return ("unhandled", None)
