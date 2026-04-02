from dataclasses import dataclass
from typing import TypedDict


class UsageExampleDict(TypedDict):
    pokemon: str
    reason: str


class ItemUsageHint(TypedDict):
    can_be_used_by: str
    good_on: list[UsageExampleDict]


@dataclass(slots=True)
class PokemonDetails:
    name: str
    total_stats: int
    is_baby: bool
    is_legendary: bool
    is_mythical: bool
    types: list[str]
    base_experience: int | None
    height: int | None
    weight: int | None


@dataclass(slots=True)
class ItemDetails:
    name: str
    display_name: str
    item: str
    type: str
    effect: str
    can_be_used_by: str
    good_on: list[UsageExampleDict]
