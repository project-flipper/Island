from pydantic import BaseModel


class Packet[T](BaseModel):
    """Generic Packet-model for incoming and outgoing event(s).

    Usage:
        Can be used either directly, as raw-packet class/object,
        or the class can be extended to give more information
        about the data being received/sent.

        Example:

        class ExampleData(BaseModel):
            example_string_data: str
            example_optional_data: int = 100
            example_optional_list: Optional[List[int]]

        ExamplePacket = Packet[ExampleData] # <-- giving more information on data structure for [d].

    Args:
        BaseModel ([type]): [description]
    """

    op: str  # packet [category:event]
    d: T  # event data
