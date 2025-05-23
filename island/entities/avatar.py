from island.entities import LocalEntity


class AvatarEntity(LocalEntity):
    @staticmethod
    async def check_color_exists(color_id: int) -> bool:
        colors = await AvatarEntity.get_all_colors()
        return color_id in colors

    @staticmethod
    async def get_all_colors() -> set[int]:
        colors_cache_exists = await AvatarEntity.cache_exists("colors")
        if not colors_cache_exists:
            # TODO: Populate the cache from database
            raise NotImplementedError()

        return await AvatarEntity.get_cache("colors")
