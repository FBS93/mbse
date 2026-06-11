from __future__ import annotations

import mbse.model.hsm as hsm

from mbse.model.hsm import HsmCallableRef
from mbse.model.hsm import HsmDocument
from mbse.model.hsm import HsmEvent
from mbse.model.hsm import HsmEventParameter
from mbse.model.hsm import HsmGuardBranch
from mbse.model.hsm import HsmGuardNode
from mbse.model.hsm import HsmInitialTransition
from mbse.model.hsm import HsmInternalTransition
from mbse.model.hsm import HsmState
from mbse.model.hsm import HsmExternalTransition
from mbse.model.hsm import HsmVariable
from mbse.model.hsm import load_hsm_document
from mbse.model.hsm import validate_hsm_document
from mbse.model.hsm.json_schema.schema_loader import load_hsm_schema as direct_load_hsm_schema
from mbse.model.hsm.model_loader import load_hsm_document as direct_load_hsm_document
from mbse.model.hsm.model_loader import validate_hsm_document as direct_validate_hsm_document
from mbse.model.hsm.model_types import HsmCallableRef as direct_hsm_callable_ref
from mbse.model.hsm.model_types import HsmDocument as direct_hsm_document
from tests.support.hsm_payloads import hsm_document
from tests.support.hsm_payloads import hsm_initial
from tests.support.hsm_payloads import hsm_state


def test_hsm_definition_module_reexports_schema_definition_types() -> None:
  assert hsm.HsmCallableRef is HsmCallableRef
  assert hsm.HsmVariable is HsmVariable
  assert hsm.HsmEventParameter is HsmEventParameter
  assert hsm.HsmEvent is HsmEvent
  assert hsm.HsmInitialTransition is HsmInitialTransition
  assert hsm.HsmExternalTransition is HsmExternalTransition
  assert hsm.HsmGuardBranch is HsmGuardBranch
  assert hsm.HsmGuardNode is HsmGuardNode
  assert hsm.HsmInternalTransition is HsmInternalTransition
  assert hsm.HsmState is HsmState
  assert hsm.HsmDocument is HsmDocument


def test_load_hsm_document_returns_definition_module_document_type() -> None:
  document = load_hsm_document(
    hsm_document(
      "door_machine",
      states=[hsm_state("closed")],
      initial_transition=hsm_initial("machine_init", "closed"),
    )
  )

  assert isinstance(document, hsm.HsmDocument)


def test_hsm_package_keeps_hsm_loader_exports_stable() -> None:
  assert load_hsm_document is direct_load_hsm_document
  assert validate_hsm_document is direct_validate_hsm_document


def test_hsm_package_reexports_new_module_layout_symbols() -> None:
  assert HsmCallableRef is direct_hsm_callable_ref
  assert HsmDocument is direct_hsm_document
  assert hsm.load_hsm_schema is direct_load_hsm_schema
