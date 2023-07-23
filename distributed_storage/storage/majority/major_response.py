import time
from collections import defaultdict
from threading import Thread, Lock, Event
from typing import Callable, Any

from distributed_storage.storage.storage import NoSuchKeyInStoragePresent


class Majority:

    def majority_result(self):
        container = defaultdict(lambda: 0)
        for element in self.elements:
            container[element] += 1
        biggest_element = max(container, key=container.get)
        return biggest_element, container[biggest_element], container

    def __init__(self, elements: list):
        self.elements = elements


def try_again_on_failure(actor, target_function, check_event):
    if check_event.isSet():
        return None
    try:
        returned = target_function(actor)
        return returned
    except Exception as exception:
        if "NoSuchKeyInStoragePresent" in str(exception):
            return None
        time.sleep(10)
        print(exception)
        return try_again_on_failure(actor, target_function, check_event)


class MajorResponse:

    def major_response(self):
        results = []
        event = Event()
        running_threads = [
            Thread(
                target=lambda actor: results.append(try_again_on_failure(actor, self.target_function, event)),
                args=(actor,)
            ).start()
            for actor in self.actors
        ]
        while len(results) == 0 \
                or (majority := Majority(results).majority_result())[1] < len(self.actors) * self.accept_threshold:
            pass
        event.set()
        return majority[0]

    def __init__(self,
                 actors: list,
                 target_function: Callable[..., Any],
                 accept_threshold: float):
        self.actors = actors
        self.target_function = target_function
        self.accept_threshold = accept_threshold
