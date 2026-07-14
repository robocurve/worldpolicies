<div align="center">

# WorldPolicies

Robocurve's registry of published robot-policy (VLA) checkpoints.

![Status: alpha](https://img.shields.io/badge/status-alpha-blue)
[![CI](https://github.com/robocurve/worldpolicies/actions/workflows/ci.yml/badge.svg)](https://github.com/robocurve/worldpolicies/actions/workflows/ci.yml)
[![Docs coverage](https://img.shields.io/badge/public%20docstrings-100%25-brightgreen)](https://github.com/robocurve/worldpolicies/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![HF Collection](https://img.shields.io/badge/🤗%20collection-WorldPolicies-yellow)](https://huggingface.co/collections/robocurve/worldpolicies-6a4dc8fd556a82aeea0fca37)
[![Benchmarks: WorldEvals](https://img.shields.io/badge/benchmarks-WorldEvals-2ea44f)](https://worldevals.org)
[![Built on Inspect Robots](https://img.shields.io/badge/eval%20with-Inspect%20Robots-indigo)](https://github.com/robocurve/inspect-robots)

</div>

Every checkpoint Robocurve publishes is indexed here. An entry records the
weights, base model, training method, training code, and an eval number with
the protocol behind it. CI validates each field, so the table below stays
accurate.

The weights themselves live on the
[robocurve Hugging Face org](https://huggingface.co/robocurve) and can be
browsed as the
[WorldPolicies Collection](https://huggingface.co/collections/robocurve/worldpolicies-6a4dc8fd556a82aeea0fca37).
Each model card follows the
[worldevals model-card standard](https://github.com/robocurve/worldevals/blob/main/docs/model-cards.md).

## Policies

| Policy | Embodiment | Base model | Method | Eval |
|---|---|---|---|---|
| [gr00t-n1.7-so101-molmoact2](https://huggingface.co/robocurve/gr00t-n1.7-so101-molmoact2) | SO-101 | [GR00T-N1.7-3B](https://huggingface.co/nvidia/GR00T-N1.7-3B) | LoRA | eval_loss 0.0273 (held-out episodes) |
| [gr00t-n1.7-yam-molmoact2](https://huggingface.co/robocurve/gr00t-n1.7-yam-molmoact2) | YAM bimanual | [GR00T-N1.7-3B](https://huggingface.co/nvidia/GR00T-N1.7-3B) | full FT | open-loop MSE 0.00279 (held-out repo) |
| [pi05-yam-molmoact2](https://huggingface.co/robocurve/pi05-yam-molmoact2) | YAM bimanual | [pi05_base](https://huggingface.co/lerobot/pi05_base) | full FT | open-loop MSE 0.00206 (held-out repo) |

Lower is better for all three metrics. Only compare rows that share a
protocol: the two YAM rows do, the SO-101 row does not. Each model card has
the details.

## Install & use

```bash
pip install "worldpolicies @ git+https://github.com/robocurve/worldpolicies"

worldpolicies list                       # all checkpoints
worldpolicies list --embodiment so101    # filter
worldpolicies info pi05-yam              # one entry in detail
```

```python
from worldpolicies import catalog, get, by_embodiment
print(get("gr00t-n17-so101").hf_url)
```

## Evaluate a policy

Serve the checkpoint (see the Usage section of its card), then drive it with
[Inspect Robots](https://github.com/robocurve/inspect-robots) through the
embodiment adapters
([SO-101](https://github.com/robocurve/inspect-robots-so101),
[YAM](https://github.com/robocurve/inspect-robots-yam)) against benchmarks
from [WorldEvals](https://worldevals.org).

## Add a checkpoint

1. Publish the model to the
   [robocurve Hugging Face org](https://huggingface.co/robocurve) with a card
   that passes the
   [model-card standard](https://github.com/robocurve/worldevals/blob/main/docs/model-cards.md).
   The checklist in the standard is gating.
2. Add it to the
   [WorldPolicies Collection](https://huggingface.co/collections/robocurve/worldpolicies-6a4dc8fd556a82aeea0fca37).
3. Append a `Policy(...)` entry to `src/worldpolicies/catalog.py`. CI
   validates every field.

Every public module, class, and function needs a docstring that states its contract rather
than restating its name; Ruff D1 enforces this in CI as part of `uv run ruff check .`.

## License

MIT for this index. Each checkpoint carries its own license, listed on its
model card.
