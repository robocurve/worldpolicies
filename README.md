<div align="center">

# 🤖 WorldPolicies

**Robocurve's registry of published robot-policy (VLA) checkpoints** — every entry
carries its eval number, protocol, training code, and a model card that passes the
[worldevals model-card standard](https://github.com/robocurve/worldevals/blob/main/docs/model-cards.md).

**WorldEvals benchmarks them; WorldPolicies is where they live.**

![Status: alpha](https://img.shields.io/badge/status-alpha-blue)
[![CI](https://github.com/robocurve/worldpolicies/actions/workflows/ci.yml/badge.svg)](https://github.com/robocurve/worldpolicies/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![HF Collection](https://img.shields.io/badge/🤗%20collection-WorldPolicies-yellow)](https://huggingface.co/collections/robocurve/worldpolicies-6a4dc8fd556a82aeea0fca37)
[![Benchmarks: WorldEvals](https://img.shields.io/badge/benchmarks-WorldEvals-2ea44f)](https://worldevals.org)
[![Built on Inspect Robots](https://img.shields.io/badge/eval%20with-Inspect%20Robots-indigo)](https://github.com/robocurve/inspect-robots)

</div>

Weights live on the [🤗 robocurve org](https://huggingface.co/robocurve) (browse the
[WorldPolicies Collection](https://huggingface.co/collections/robocurve/worldpolicies-6a4dc8fd556a82aeea0fca37));
this repo is the **validated index** — CI fails on malformed entries, so the table below
can be trusted.

## Policies

| Policy | Embodiment | Base model | Method | Eval | Trained by |
|---|---|---|---|---|---|
| [gr00t-n1.7-so101-molmoact2](https://huggingface.co/robocurve/gr00t-n1.7-so101-molmoact2) | SO-101 | [GR00T-N1.7-3B](https://huggingface.co/nvidia/GR00T-N1.7-3B) | LoRA | eval_loss **0.0273** (held-out episodes) | jeqcho |
| [gr00t-n1.7-yam-molmoact2](https://huggingface.co/robocurve/gr00t-n1.7-yam-molmoact2) | YAM bimanual | [GR00T-N1.7-3B](https://huggingface.co/nvidia/GR00T-N1.7-3B) | full FT | open-loop MSE **0.00279** (held-out repo) | aris |
| [pi05-yam-molmoact2](https://huggingface.co/robocurve/pi05-yam-molmoact2) | YAM bimanual | [pi05_base](https://huggingface.co/lerobot/pi05_base) | full FT | open-loop MSE **0.00206** (held-out repo) | aris |

Metrics are lower-is-better and are **not comparable across rows** unless the protocol
matches — the two YAM rows share a protocol; the SO-101 row does not. Details on each card.

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

Serve the checkpoint (see its card's Usage section), then drive it with
[Inspect Robots](https://github.com/robocurve/inspect-robots) via the embodiment adapters
([SO-101](https://github.com/robocurve/inspect-robots-so101) ·
[YAM](https://github.com/robocurve/inspect-robots-yam)) against benchmarks from
[WorldEvals](https://worldevals.org).

## Add a checkpoint

1. Publish the model to the [🤗 robocurve org](https://huggingface.co/robocurve) with a card
   passing the [model-card standard](https://github.com/robocurve/worldevals/blob/main/docs/model-cards.md)
   (checklist is gating).
2. Add it to the [WorldPolicies Collection](https://huggingface.co/collections/robocurve/worldpolicies-6a4dc8fd556a82aeea0fca37).
3. Append a `Policy(...)` entry to `src/worldpolicies/catalog.py` — CI validates every field.

## License

MIT (the index). Each checkpoint carries its own license — see its model card.
