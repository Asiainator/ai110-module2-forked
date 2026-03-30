from datetime import date, timedelta

from pawpal_system import OwnerInfo, Pet, RigidTask, StaticTask, Scheduler


def test_mark_complete_updates_status() -> None:
    task = RigidTask(
        name="Walk",
        description="Morning walk",
        duration=30,
        ideal_time="08:00",
        priority=5,
    )

    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_adding_task_increases_task_count() -> None:
    pet = Pet(name="Milo", birthday="2021-04-14", animal="Dog")
    initial_count = pet.task_count

    task = StaticTask(
        name="Medication",
        description="Give medication at 09:00",
        duration=10,
        ideal_time="09:00",
        fixed_time="09:00",
    )

    pet.add_task(task)

    assert pet.task_count == initial_count + 1


def test_filter_tasks_by_completion() -> None:
    owner = OwnerInfo(name="Anato")
    pet = Pet(name="Milo", birthday="2021-04-14", animal="Dog")

    completed_task = RigidTask(
        name="Walk",
        description="Morning walk",
        duration=30,
        ideal_time="08:00",
        priority=5,
    )
    completed_task.mark_complete()

    incomplete_task = RigidTask(
        name="Play",
        description="Playtime",
        duration=15,
        ideal_time="10:00",
        priority=3,
    )

    pet.add_task(completed_task)
    pet.add_task(incomplete_task)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    completed = scheduler.filter_tasks_by_completion(True)
    incomplete = scheduler.filter_tasks_by_completion(False)

    assert len(completed) == 1
    assert completed[0][1].completed is True
    assert len(incomplete) == 1
    assert incomplete[0][1].completed is False


def test_detect_static_conflicts_returns_warning() -> None:
    owner = OwnerInfo(name="Anato")
    pet = Pet(name="Milo", birthday="2021-04-14", animal="Dog")
    task_date = date(2026, 3, 29)

    task1 = StaticTask(
        name="Morning meds",
        description="Give medication",
        duration=10,
        ideal_time="09:00",
        fixed_time="09:00",
        task_date=task_date,
    )
    task2 = StaticTask(
        name="Breakfast",
        description="Feed Milo",
        duration=15,
        ideal_time="09:00",
        fixed_time="09:00",
        task_date=task_date,
    )

    pet.add_task(task1)
    pet.add_task(task2)
    owner.add_pet(pet)

    scheduler = Scheduler(owner)
    warnings = scheduler.detect_static_conflicts()

    assert len(warnings) == 1
    assert "Milo has 2 static tasks scheduled at 2026-03-29 09:00" in warnings[0]


def test_daily_task_recreates_after_completion() -> None:
    owner = OwnerInfo(name="Anato")
    pet = Pet(name="Milo", birthday="2021-04-14", animal="Dog")
    start_date = date(2026, 3, 29)

    daily_task = RigidTask(
        name="Daily walk",
        description="Take Milo on a daily walk",
        duration=30,
        ideal_time="08:00",
        priority=5,
        daily=True,
        task_date=start_date,
    )

    pet.add_task(daily_task)
    owner.add_pet(pet)

    daily_task.mark_complete(parent_pet=pet)

    assert daily_task.completed is True
    assert pet.task_count == 2
    new_task = pet.list_tasks()[-1]
    assert new_task.name == "Daily walk"
    assert new_task.completed is False
    assert new_task.daily is True
    assert new_task.date == start_date + timedelta(days=1)


