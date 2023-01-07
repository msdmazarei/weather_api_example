from datetime import datetime


def to_epoch(dt: datetime = datetime.utcnow()) -> int:
    return int(dt.timestamp())


def to_epoch_us(dt: datetime = datetime.utcnow()) -> int:
    return int(dt.timestamp() * 1000000)


def from_epoch_us(epoch: int) -> datetime:
    return datetime.fromtimestamp(epoch / 1000000)


def from_epoch(epoch: int) -> datetime:
    return datetime.fromtimestamp(epoch)
