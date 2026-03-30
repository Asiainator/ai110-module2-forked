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


