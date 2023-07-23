from collections import defaultdict
from threading import Thread, Lock
from typing import Callable, Any


class Majority:

    def majority_result(self):
        container = defaultdict(lambda: 0)
        for element in self.elements:
            print(element)
            print(hash(element))
            print(container[element])
            container[element] += 1
        biggest_element = max(container, key=container.get)
        return biggest_element, container[biggest_element]

    def __init__(self, elements: list):
        self.elements = elements


class MajorResponse:

    def major_response(self):
        results = []
        running_threads = [
            Thread(
                target=lambda actor: results.append(self.target_function(actor)),
                args=(actor,)
            ).start()
            for actor in self.actors
        ]
        while len(results) == 0 \
                or (majority := Majority(results).majority_result())[1] < len(self.actors) * self.accept_threshold:
            pass
        return majority[0]

    def __init__(self,
                 actors: list,
                 target_function: Callable[..., Any],
                 accept_threshold: float):
        self.actors = actors
        self.target_function = target_function
        self.accept_threshold = accept_threshold
