from pydantic import BaseModel


class MascotOptions(BaseModel):
    igrator_active: bool


class PartyOptions(BaseModel):
    fair_ticket_active: bool
    hunt_active: bool
    itemRewardID: int
    isMapNoteActive: bool
    showPartyAnnouncement: bool
    party_icon_active: bool


class IglooOptions(BaseModel):
    contestRunning: bool


class IslandOptions(BaseModel):
    isDaytime: bool


class OopsTest(BaseModel):
    testEnabled: bool


class GeneralConfig(BaseModel):
    mascot_options: MascotOptions
    party_options: PartyOptions
    igloo_options: IglooOptions
    oops_test: OopsTest
    island_options: IslandOptions
    party_dates: dict[str, str]


class RoomConfig(BaseModel):
    room_id: int
    room_key: str
    name: str
    display_name: str
    music_id: int
    is_member: bool
    path: str
    max_users: int
    jump_enabled: bool
    required_item: int | None
    short_name: str
    pin_id: int | None
    pin_x: int | None
    pin_y: int
    safe_start_x: int
    safe_end_x: int
    safe_start_y: int
    safe_end_y: int


class PaperItemConfig(BaseModel):
    paper_item_id: int
    type: int
    cost: int
    is_member: bool
    label: str
    prompt: str
    layer: int
    is_epf: bool | None
    custom_depth: int | None
    has_translations: bool | None
    is_back: bool | None
    has_back: bool | None
    make_tour_guide: bool | None
    make_secret_agent: bool | None
    is_medal: bool | None
    is_gift: bool | None
    no_purchase_popup: bool | None
    exclusive: int | None
    is_bait: bool | None
    is_game_achievable: bool | None


class GameConfig(BaseModel):
    game_key: str
    name: str
    room_id: int
    music_id: int
    stamp_group_id: int
    path: str
    show_player_in_room: bool
    is_hybrid: bool
