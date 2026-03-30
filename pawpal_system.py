from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional


class OwnerInfo:
    def __init__(self, name: str, pets: Optional[List[Pet]] = None):
        self.name = name
        self.pets = pets or []

    def add_pet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def list_pets(self) -> List[Pet]:
        return self.pets


class Pet:
    def __init__(self, name: str, birthday: str, animal: str):
        self.name = name
        self.birthday = birthday
        self.animal = animal


class Task(ABC):
    def __init__(self, duration: int, ideal_time: str):
        self.duration = duration
        self.ideal_time = ideal_time

    @abstractmethod
    def describe(self) -> str:
        raise NotImplementedError


class RigidTask(Task):
    def __init__(self, duration: int, ideal_time: str, priority: int):
        super().__init__(duration, ideal_time)
        self.priority = priority

    def describe(self) -> str:
        return f"RigidTask(duration={self.duration}, ideal_time={self.ideal_time}, priority={self.priority})"


class StaticTask(Task):
    def __init__(self, duration: int, ideal_time: str, fixed_time: str):
        super().__init__(duration, ideal_time)
        self.fixed_time = fixed_time

    def describe(self) -> str:
        return f"StaticTask(duration={self.duration}, ideal_time={self.ideal_time}, fixed_time={self.fixed_time})"
