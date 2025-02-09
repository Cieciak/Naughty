from copy import copy

class PostQueue:

    def __init__(self, target: int):
        self.__queue = list()
        self.pointer: int = 0
        
        self.target: int = target

    @property
    def empty(self) -> bool:
        return len(self.__queue) - self.pointer == 0

    @property
    def length(self) -> int:
        return len(self.__queue)

    def __repr__(self):
        return f'Queue[{self.pointer}, targets {self.target}]'

    def append(self, single, /):
        self.__queue.append(single)

    def extend(self, multiple, /):
        self.__queue.extend(multiple)

    def pop(self):
        post = self.__queue[self.pointer]

        # If we reached the target, drop the oldest image
        if self.pointer == self.target:
            self.__queue.pop(0)
        # If we overshoot the target drop until the are at target
        elif self.pointer >= self.target:
            diff = self.pointer - self.target
            self.__queue = self.__queue[diff:]
            self.pointer -= diff
        # If we haven't reached the target yet, advance the pointer 
        else:
            self.pointer += 1

        return post

    def flush(self):
        self.__queue = list()
