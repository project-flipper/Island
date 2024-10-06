from island.entities.world import BaseWorldEntity


class RoomEntity(BaseWorldEntity):
    @classmethod
    async def check_player_exists(cls, player_id: int, *, room_id: int) -> bool:
        player_ids = await cls.get_all_player_ids(room_id=room_id)
        return player_id in player_ids

    @classmethod
    async def get_all_player_ids(cls, *, room_id: int) -> set[int]:
        key = f"rooms.{room_id}"

        colors_cache_exists = await cls.cache_exists(key)
        if not colors_cache_exists:
            # TODO: Populate the cache from database
            raise NotImplementedError()

        players = await cls.get_cache(key, command="smembers")
        return set(map(int, players))
