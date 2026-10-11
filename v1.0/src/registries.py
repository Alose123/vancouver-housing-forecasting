"""Registries represent executable capabilities, not a predetermined winner."""
from dataclasses import dataclass
from types import MappingProxyType
from typing import Callable


def naive(values: list[float], horizon: int):
    if not values or horizon <= 0:
        raise ValueError("Naive requires history and a positive horizon.")
    return [values[-1]] * horizon


def seasonal_naive(values: list[float], horizon: int):
    if len(values) < 12 or horizon <= 0:
        raise ValueError("Seasonal naive requires at least 12 monthly observations.")
    return [values[-12 + i % 12] for i in range(horizon)]


@dataclass(frozen=True)
class ModelSpec:
    name: str
    description: str
    function: Callable
    baseline: bool
    fitted_preprocessing: bool = False


MODEL_REGISTRY = MappingProxyType({
    "naive": ModelSpec("naive", "Repeat the last known monthly price.", naive, True),
    "seasonal_naive": ModelSpec("seasonal_naive", "Repeat the last known 12 months.",
                                seasonal_naive, True),
})
REGIME_REGISTRY = MappingProxyType({})
PROPOSED_CAPABILITIES = {
    "forecast": ["ridge", "autoregression", "random_forest", "gradient_boosting", "SARIMA"],
    "regime": ["kmeans", "gmm", "hierarchical"],
}


class CapabilityRequest(ValueError):
    """An unregistered method is a human-review request, never an installation."""


def require_model(name: str):
    if name not in MODEL_REGISTRY:
        raise CapabilityRequest(f"Model {name!r} is not registered.")
    return MODEL_REGISTRY[name]


def require_regime_method(name: str):
    if name not in REGIME_REGISTRY:
        raise CapabilityRequest(f"Regime method {name!r} is not registered.")
    return REGIME_REGISTRY[name]
