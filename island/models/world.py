from pydantic import BaseModel

from island.database.schema.world import WorldTable


class World(BaseModel):
    id: int
    name: str
    population: int
    safeChat: bool
    buddies: bool
    url: str

    @staticmethod
    def compute_population(population: int, capacity: int) -> int:
        if population >= capacity:
            return 5

        return max(round(5 * (population / capacity)), 1)

    @classmethod
    async def from_table(cls, world: WorldTable) -> "World":
        # TODO: get population, buddies and url
        return cls(
            id=world.id,
            name=world.name,
            population=cls.compute_population(0, world.capacity),
            safeChat=world.is_safe,
            buddies=False,
            url="localhost",
        )
