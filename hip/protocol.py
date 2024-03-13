import typing
import bittensor as bt

class HIPProtocol(bt.Synapse):
    # Required fields
    data: str
    uid: int

    # Optional fields
    response: typing.Optional[str] = None
    consensus: typing.Optional[str] = None
    weights: typing.Optional[typing.List[float]] = None

    def serialize(self) -> bytes:
        """
        Serialize the HIPProtocol instance to bytes.
        """
        return bt.serialize(self)

    @classmethod
    def deserialize(cls, data: bytes) -> 'HIPProtocol':
        """
        Deserialize bytes to a HIPProtocol instance.
        """
        return bt.deserialize(data, HIPProtocol)