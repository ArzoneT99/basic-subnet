import typing
import bittensor as bt
import time


class HIPProtocol(bt.Synapse):
    # Added extra fields to handle api
    id: str
    timestamp: float = time.time()
    label: str
    type: str
    value: str
    image: typing.Optional[str] = None
    options: typing.Optional[typing.List[str]] = None
    uid: int
    question_id: int
    question: typing.Optional[str] = None
    answer: typing.Optional[str] = None
    response: typing.Optional[str] = None
    reward: typing.Optional[float] = None
    consensus: typing.Optional[str] = None

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