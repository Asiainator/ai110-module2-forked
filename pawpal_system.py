from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Optional


class OwnerInfo:
    def __init__(self, name: str, pets: Optional[List[Pet]] = None):
        """Create an owner and optionally attach a list of pets."""
        self.name = name
        self.pets = pets or []
        self.pet_count = len(self.pets)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        self.pets.append(pet)
        self.pet_count = len(self.pets)

    def list_pets(self) -> List[Pet]:
        """Return the list of pets for this owner."""
        return self.pets


class Pet:
    def __init__(self, name: str, birthday: str, animal: str, tasks: Optional[List[Task]] = None):
        """Create a pet and optionally initialize its task list."""
        self.name = name
        self.birthday = birthday
        self.animal = animal
        self.tasks = tasks or []
        self.task_count = len(self.tasks)

    def add_task(self, task: Task) -> None:
        """Attach a task to the pet's task list."""
        self.tasks.append(task)
        self.task_count = len(self.tasks)

    def list_tasks(self) -> List[Task]:
        """Return the pet's current tasks."""
        return self.tasks


class Task(ABC):
    def __init__(self, name: str, description: str, duration: int, ideal_time: str):
        """Initialize the shared task fields for every task type."""
        self.name = name
        self.description = description
        self.duration = duration
        self.ideal_time = ideal_time
        self.completed = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    @abstractmethod
    def describe(self) -> str:
        """Return a text description of this task."""
        raise NotImplementedError


class RigidTask(Task):
    def __init__(self, name: str, description: str, duration: int, ideal_time: str, priority: int):
        """Create a rigid task with a priority and ideal time."""
        super().__init__(name, description, duration, ideal_time)
        self.priority = priority

    def describe(self) -> str:
        """Return a description string for the rigid task."""
        return (
            f"RigidTask(name={self.name}, description={self.description}, "
            f"duration={self.duration}, ideal_time={self.ideal_time}, priority={self.priority})"
        )


class StaticTask(Task):
    def __init__(self, name: str, description: str, duration: int, ideal_time: str, fixed_time: str):
        """Create a static task that should occur at a fixed time."""
        super().__init__(name, description, duration, ideal_time)
        self.fixed_time = fixed_time

    def describe(self) -> str:
        """Return a description string for the static task."""
        return (
            f"StaticTask(name={self.name}, description={self.description}, "
            f"duration={self.duration}, ideal_time={self.ideal_time}, fixed_time={self.fixed_time})"
        )


class Scheduler:
    def __init__(self, owner: OwnerInfo):
        """Create a scheduler for the given owner."""
        self.owner = owner

    def schedule_tasks(self) -> List[tuple[Pet, Task]]:
        """Build and return a sorted schedule for all tasks across the owner's pets."""
        schedule: List[tuple[Pet, Task]] = []
        for pet in self.owner.list_pets():
            for task in pet.list_tasks():
                schedule.append((pet, task))

        schedule.sort(key=lambda pair: self._task_sort_key(pair[1]))
        return schedule

    def _task_sort_key(self, task: Task) -> tuple[int, str, int]:
        """Return a sort key that prioritizes static tasks first, then rigid tasks."""
        if isinstance(task, StaticTask):
            return (0, task.fixed_time, 0)
        if isinstance(task, RigidTask):
            return (1, task.ideal_time, -task.priority)
        return (2, task.ideal_time, 0)
