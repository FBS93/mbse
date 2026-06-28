from __future__ import annotations


def is_ready(ctx) -> bool:
  """Return whether the reference activity should execute its action path."""

  return getattr(ctx, "is_ready", True)


def prepare_output(ctx) -> None:
  """Record that the reference activity action was executed."""

  ctx.output_prepared = True


def set_result_true(ctx) -> None:
  """Set the shared model-call result variable to true."""

  ctx.result = True


def return_not_bool(ctx) -> str:
  """Return an invalid decision result for runtime error tests."""

  return "not-bool"
