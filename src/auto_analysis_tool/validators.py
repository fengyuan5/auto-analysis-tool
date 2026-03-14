from __future__ import annotations

ALLOWED_MODES = {"infer", "train", "train_infer"}
ALLOWED_DOMAINS = {
    "llm",
    "multimodal",
    "spatial_intelligence",
    "embodied_intelligence",
    "recsys",
    "other",
}
ALLOWED_ENTRYPOINT_TYPES = {"shell", "python"}
ALLOWED_PROFILING_ENABLE_MODES = {"none", "flag", "env", "external"}

REQUIRED_RECIPE_KEYS = [
    "recipe_name",
    "model_name",
    "task_type",
    "mode",
    "domain",
    "hardware_target",
    "cann_version",
    "framework",
    "python_version",
    "entrypoint",
    "outputs",
    "profiling",
    "metrics",
    "comparison_baseline",
    "baseline_run_id",
    "optimized_run_id",
]


def validate_recipe_data(data: dict) -> list[str]:
    errors: list[str] = []

    for key in REQUIRED_RECIPE_KEYS:
        if key not in data:
            errors.append(f"missing required field: {key}")

    mode = data.get("mode")
    if mode is not None and mode not in ALLOWED_MODES:
        errors.append(f"invalid mode: {mode}")

    domain = data.get("domain")
    if domain is not None and domain not in ALLOWED_DOMAINS:
        errors.append(f"invalid domain: {domain}")

    entrypoint = data.get("entrypoint", {})
    for key in ["type", "path", "workdir", "default_args"]:
        if key not in entrypoint:
            errors.append(f"missing entrypoint field: {key}")
    entrypoint_type = entrypoint.get("type")
    if entrypoint_type is not None and entrypoint_type not in ALLOWED_ENTRYPOINT_TYPES:
        errors.append(f"invalid entrypoint.type: {entrypoint_type}")
    default_args = entrypoint.get("default_args")
    if default_args is not None and not isinstance(default_args, list):
        errors.append("entrypoint.default_args must be a list")

    outputs = data.get("outputs", {})
    for key in ["log_dir", "result_dir", "checkpoint_dir"]:
        if key not in outputs:
            errors.append(f"missing outputs field: {key}")

    profiling = data.get("profiling", {})
    for key in ["supported", "enable_mode", "enable_flag", "notes"]:
        if key not in profiling:
            errors.append(f"missing profiling field: {key}")
    profiling_enable_mode = profiling.get("enable_mode")
    if (
        profiling_enable_mode is not None
        and profiling_enable_mode not in ALLOWED_PROFILING_ENABLE_MODES
    ):
        errors.append(f"invalid profiling.enable_mode: {profiling_enable_mode}")

    metrics = data.get("metrics", {})
    for key in ["performance", "accuracy"]:
        if key not in metrics:
            errors.append(f"missing metrics field: {key}")
    for key in ["performance", "accuracy"]:
        value = metrics.get(key)
        if value is not None and not isinstance(value, list):
            errors.append(f"metrics.{key} must be a list")

    for key in ["baseline_run_id", "optimized_run_id", "comparison_baseline", "recipe_name"]:
        value = data.get(key)
        if value is not None and not isinstance(value, str):
            errors.append(f"{key} must be a string")

    return errors
