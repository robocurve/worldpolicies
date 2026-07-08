"""The WorldPolicies catalog: Robocurve's registry of published robot-policy checkpoints.

Every entry points at a HuggingFace model repo whose card follows the
worldevals model-card standard
(https://github.com/robocurve/worldevals/blob/main/docs/model-cards.md).
Entries are validated by tests/test_catalog.py — a malformed entry fails CI.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Policy:
    """One published checkpoint."""

    name: str
    """Short unique key, e.g. ``gr00t-n17-so101``."""

    hf_id: str
    """HuggingFace model id, e.g. ``robocurve/gr00t-n1.7-so101-molmoact2``."""

    title: str
    """One-line human title."""

    description: str
    """Two-to-three sentence summary (base model, method, data)."""

    base_model: str
    """HuggingFace id of the base checkpoint."""

    embodiment: str
    """Robot platform key, e.g. ``so101`` or ``yam-bimanual``."""

    method: str
    """``lora`` or ``full-ft``."""

    framework: str
    """Training framework, e.g. ``isaac-gr00t`` or ``openpi``."""

    eval_metric: str
    """Primary metric name, e.g. ``open_loop_mse`` or ``eval_loss``."""

    eval_value: float
    """Primary metric value (lower is better for both metrics above)."""

    eval_protocol: str
    """One-line protocol description; details live on the model card."""

    training_repo: str
    """GitHub URL of the training code (may be private; still record it)."""

    trained_by: str
    """Person/team credited on the model card."""

    tags: tuple[str, ...] = field(default_factory=tuple)
    """Free-form tags for filtering, e.g. ("vla", "bimanual")."""

    @property
    def hf_url(self) -> str:
        """Full HuggingFace URL for this checkpoint."""
        return f"https://huggingface.co/{self.hf_id}"


CATALOG: tuple[Policy, ...] = (
    Policy(
        name="gr00t-n17-so101",
        hf_id="robocurve/gr00t-n1.7-so101-molmoact2",
        title="GR00T N1.7 x SO-101 (MolmoAct2 community data, LoRA)",
        description=(
            "LoRA fine-tune of nvidia/GR00T-N1.7-3B for the SO-101 follower arm on 39 "
            "community LeRobot repos (2,242 episodes) filtered from the MolmoAct2 "
            "SO-100/101 manifest, with annotated language instructions. Adapters merged; "
            "raw adapters shipped alongside."
        ),
        base_model="nvidia/GR00T-N1.7-3B",
        embodiment="so101",
        method="lora",
        framework="isaac-gr00t",
        eval_metric="eval_loss",
        eval_value=0.0273,
        eval_protocol="held-out flow-matching loss, episode-level 5% split across all 39 repos",
        training_repo="https://github.com/robocurve/gr00t-n1.7-so-101",
        trained_by="jeqcho",
        tags=("vla", "gr00t", "single-arm", "community-data"),
    ),
    Policy(
        name="gr00t-n17-yam",
        hf_id="robocurve/gr00t-n1.7-yam-molmoact2",
        title="GR00T N1.7 x YAM bimanual (MolmoAct2, full fine-tune)",
        description=(
            "Full fine-tune (action head + projector) of nvidia/GR00T-N1.7-3B on the "
            "AllenAI MolmoAct2-BimanualYAM dataset (124 repos, ~5,145 episodes) for the "
            "I2RT YAM bimanual platform."
        ),
        base_model="nvidia/GR00T-N1.7-3B",
        embodiment="yam-bimanual",
        method="full-ft",
        framework="isaac-gr00t",
        eval_metric="open_loop_mse",
        eval_value=0.00279,
        eval_protocol="open-loop action MSE on held-out repo allenai/19012026-block-13",
        training_repo="https://github.com/robocurve/gr00t-n17-yam-replication",
        trained_by="aris",
        tags=("vla", "gr00t", "bimanual"),
    ),
    Policy(
        name="pi05-yam",
        hf_id="robocurve/pi05-yam-molmoact2",
        title="pi0.5 x YAM bimanual (MolmoAct2, full fine-tune)",
        description=(
            "JAX/openpi full fine-tune of pi05_base on the AllenAI MolmoAct2-BimanualYAM "
            "dataset for the I2RT YAM bimanual platform. Orbax checkpoint (EMA weights)."
        ),
        base_model="lerobot/pi05_base",
        embodiment="yam-bimanual",
        method="full-ft",
        framework="openpi",
        eval_metric="open_loop_mse",
        eval_value=0.00206,
        eval_protocol="open-loop action MSE on held-out repo allenai/19012026-block-13",
        training_repo="https://github.com/robocurve/pi05-yam-replication",
        trained_by="aris",
        tags=("vla", "pi05", "bimanual"),
    ),
)


def catalog() -> tuple[Policy, ...]:
    """All catalogued policies."""
    return CATALOG


def get(name: str) -> Policy:
    """Look up a policy by its short key. Raises ``KeyError`` if absent."""
    for policy in CATALOG:
        if policy.name == name:
            return policy
    raise KeyError(f"no policy named {name!r}; known: {[p.name for p in CATALOG]}")


def by_embodiment(embodiment: str) -> tuple[Policy, ...]:
    """Policies for a given embodiment key."""
    return tuple(p for p in CATALOG if p.embodiment == embodiment)


def by_tag(tag: str) -> tuple[Policy, ...]:
    """Policies carrying a given tag."""
    return tuple(p for p in CATALOG if tag in p.tags)
