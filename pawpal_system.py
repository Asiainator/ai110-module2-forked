from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import date, timedelta
from typing import List, Optional


class OwnerInfo:
    def __init__(self, name: str, pets: Optional[List[Pet]] = None):
        """Create an owner and optionally attach a list of pets."""
        self.name = name
        self.pets = pets or []

    @property
    def pet_count(self) -> int:
        """Return the number of pets owned."""
        return len(self.pets)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner's pet list."""
        self.pets.append(pet)

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

    @property
    def task_count(self) -> int:
        """Return the number of tasks assigned to this pet."""
        return len(self.tasks)

    def add_task(self, task: Task) -> None:
        """Attach a task to the pet's task list."""
        self.tasks.append(task)

    def list_tasks(self) -> List[Task]:
        """Return the pet's current tasks."""
        return self.tasks


class Task(ABC):
    def __init__(
        self,
        name: str,
        description: str,
        duration: int,
        ideal_time: str,
        daily: bool = False,
        task_date: Optional[date] = None,
    ):
        """Initialize the shared task fields for every task type."""
        self.name = name
        self.description = description
        self.duration = duration
        self.ideal_time = ideal_time
        self.daily = daily
        self.date = task_date or date.today()
        self.completed = False

    def mark_complete(self, parent_pet: Optional[Pet] = None) -> None:
        """Mark this task as completed.

        If the task is daily and the parent pet is provided, clone the task
        and add a fresh copy back to the pet with the next date.
        """
        self.completed = True
        if self.daily and parent_pet is not None:
            parent_pet.add_task(self.clone(next_day=True))

    def _clone_date(self, next_day: bool) -> date:
        return self.date + timedelta(days=1) if next_day else self.date

    @abstractmethod
    def clone(self, next_day: bool = False) -> Task:
        """Return a copy of this task for daily repeat scheduling."""
        raise NotImplementedError

    @abstractmethod
    def describe(self) -> str:
        """Return a text description of this task."""
        raise NotImplementedError


class RigidTask(Task):
    def __init__(
        self,
        name: str,
        description: str,
        duration: int,
        ideal_time: str,
        priority: int,
        daily: bool = False,
        task_date: Optional[date] = None,
    ):
        """Create a rigid task with a priority and ideal time."""
        super().__init__(name, description, duration, ideal_time, daily=daily, task_date=task_date)
        self.priority = priority

    def clone(self, next_day: bool = False) -> RigidTask:
        return RigidTask(
            name=self.name,
            description=self.description,
            duration=self.duration,
            ideal_time=self.ideal_time,
            priority=self.priority,
            daily=self.daily,
            task_date=self._clone_date(next_day),
        )

    def describe(self) -> str:
        """Return a description string for the rigid task."""
        return (
            f"RigidTask(name={self.name}, description={self.description}, "
            f"duration={self.duration}, ideal_time={self.ideal_time}, priority={self.priority})"
        )


class StaticTask(Task):
    def __init__(
        self,
        name: str,
        description: str,
        duration: int,
        ideal_time: str,
        fixed_time: str,
        daily: bool = False,
        task_date: Optional[date] = None,
    ):
        """Create a static task that should occur at a fixed time."""
        super().__init__(name, description, duration, ideal_time, daily=daily, task_date=task_date)
        self.fixed_time = fixed_time

    def clone(self, next_day: bool = False) -> StaticTask:
        return StaticTask(
            name=self.name,
            description=self.description,
            duration=self.duration,
            ideal_time=self.ideal_time,
            fixed_time=self.fixed_time,
            daily=self.daily,
            task_date=self._clone_date(next_day),
        )

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
        """Build and return a schedule sorted by each task's time."""
        schedule: List[tuple[Pet, Task]] = []
        for pet in self.owner.list_pets():
            for task in pet.list_tasks():
                schedule.append((pet, task))

        return self.sort_by_time(schedule)

    def filter_tasks_by_completion(self, completed: bool) -> List[tuple[Pet, Task]]:
        """Return only the tasks whose completion status matches the requested value."""
        return [
            pair
            for pair in self.schedule_tasks()
            if pair[1].completed == completed
        ]

    def sort_by_time(self, schedule: List[tuple[Pet, Task]]) -> List[tuple[Pet, Task]]:
        """Return the schedule sorted by date and each task's HH:MM time string."""
        return sorted(
            schedule,
            key=lambda pair: (
                pair[1].date,
                getattr(pair[1], "fixed_time", pair[1].ideal_time),
            ),
        )

    def detect_static_conflicts(self) -> List[str]:
        """Detect same-pet static task conflicts and return warnings."""
        warnings: List[str] = []
        for pet in self.owner.list_pets():
            tasks_by_slot: dict[tuple[date, str], List[StaticTask]] = {}
            for task in pet.list_tasks():
                if isinstance(task, StaticTask):
                    slot = (task.date, task.fixed_time)
                    tasks_by_slot.setdefault(slot, []).append(task)

            for (task_date, fixed_time), tasks in tasks_by_slot.items():
                if len(tasks) > 1:
                    task_names = ", ".join(task.name for task in tasks)
                    warnings.append(
                        f"Warning: {pet.name} has {len(tasks)} static tasks scheduled at "
                        f"{task_date.isoformat()} {fixed_time}: {task_names}"
                    )
        return warnings

    def _task_sort_key(self, task: Task) -> tuple[int, str, int]:
        """Return a sort key that prioritizes static tasks first, then rigid tasks."""
        if isinstance(task, StaticTask):
            return (0, task.fixed_time, 0)
        if isinstance(task, RigidTask):
            return (1, task.ideal_time, -task.priority)
        return (2, task.ideal_time, 0)
