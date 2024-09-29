from __future__ import annotations

from pydantic import BaseModel

from island.database.schema.world import WorldTable


class World(BaseModel):
    id: int
    name: str
    population: int
    safe_chat: bool
    buddies: bool
    url: str

    @staticmethod
    def compute_population(population: int, capacity: int) -> int:
        if population >= capacity:
            return 5

        return max(round(5 * (population / capacity)), 1)

    @classmethod
    async def from_table(cls, world: WorldTable, *, population: int, has_buddies: bool) -> World:
        # TODO: get population and buddies
        return cls(
            id=world.id,
            name=world.name,
            population=cls.compute_population(population, world.capacity),
            safe_chat=world.is_safe,
            buddies=has_buddies,
            url=world.url,
        )
