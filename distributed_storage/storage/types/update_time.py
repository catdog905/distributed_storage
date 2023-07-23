from google.protobuf.timestamp_pb2 import Timestamp as StubTimestamp
from datetime import datetime
import time


class UpdateTime:
    def __init__(self, seconds, nanos):
        self.seconds = seconds
        self.nanos = nanos

    def __hash__(self):
        return hash(self.seconds) + hash(self.nanos)

    def __eq__(self, other):
        return self.seconds < other.seconds and self.nanos == other.nanos

    def __lt__(self, other):
        return self.seconds < other.seconds or (self.seconds == other.seconds and self.nanos < other.nanos)

    def __le__(self, other):
        return self.seconds <= other.seconds or (self.seconds == other.seconds and self.nanos <= other.nanos)

    def __gt__(self, other):
        return self.seconds > other.seconds or (self.seconds == other.seconds and self.nanos > other.nanos)

    def __ge__(self, other):
        return self.seconds >= other.seconds or (self.seconds == other.seconds and self.nanos >= other.nanos)

    def __ne__(self, other):
        return self.seconds != other.seconds or self.nanos != other.nanos


class UpdateTimeFromTimeNs(UpdateTime):
    def __init__(self, time_ns):
        super().__init__(time_ns // 10 ** 9, time_ns - (time_ns // 10 ** 9 * 10**9))

    def __hash__(self):
        return super.__hash__(super)

    def __eq__(self, other):
        return super.__eq__(super, other)


class CurrentUpdateTime(UpdateTimeFromTimeNs):
    def __init__(self):
        super().__init__(time.time_ns())

    def __hash__(self):
        return super.__hash__(super)

    def __eq__(self, other):
        return super.__eq__(super, other)


class StubTimestampFromUpdateTime:
    def __init__(self, timestamp: UpdateTime):
        self.seconds = timestamp.seconds
        self.nanos = timestamp.nanos

    def stub(self) -> StubTimestamp:
        return StubTimestamp(seconds=self.seconds, nanos=self.nanos)