from google.protobuf.timestamp_pb2 import Timestamp as StubTimestamp
from datetime import datetime
import time


class UpdateTime:
    def __init__(self, seconds, nanos):
        self.seconds = seconds
        self.nanos = nanos


class UpdateTimeFromTimeNs(UpdateTime):
    def __init__(self, time_ns):
        super().__init__(time_ns // 10 ** 9, time_ns - (time_ns // 10 ** 9 * 10**9))


class CurrentUpdateTime(UpdateTimeFromTimeNs):
    def __init__(self):
        super().__init__(time.time_ns())


class StubTimestampFromUpdateTime:
    def __init__(self, timestamp: UpdateTime):
        self.seconds = timestamp.seconds
        self.nanos = timestamp.nanos

    def stub(self) -> StubTimestamp:
        return StubTimestamp(seconds=self.seconds, nanos=self.nanos)