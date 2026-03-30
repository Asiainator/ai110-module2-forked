from pawpal_system import OwnerInfo, Pet, RigidTask, StaticTask, Scheduler


def main() -> None:
    owner = OwnerInfo(name="Anato")

    pet1 = Pet(name="Milo", birthday="2021-04-14", animal="Dog")
    pet2 = Pet(name="Luna", birthday="2022-09-03", animal="Cat")

    task1 = RigidTask(
        name="Morning walk",
        description="Take Milo for a 30-minute walk",
        duration=30,
        ideal_time="08:00",
        priority=5,
    )

    task2 = StaticTask(
        name="Medication",
        description="Give Luna her fixed 09:00 medication",
        duration=10,
        ideal_time="09:00",
        fixed_time="09:00",
    )

    task3 = RigidTask(
        name="Evening feeding",
        description="Feed Milo before bedtime",
        duration=20,
        ideal_time="20:00",
        priority=3,
    )

    pet1.add_task(task1)
    pet1.add_task(task3)
    pet2.add_task(task2)

    owner.add_pet(pet1)
    owner.add_pet(pet2)

    scheduler = Scheduler(owner)
    schedule = scheduler.schedule_tasks()

    print("Today's schedule:")
    for pet, task in schedule:
        print(f"- {pet.name}: {task.name} at {getattr(task, 'fixed_time', task.ideal_time)} ({task.description})")


if __name__ == "__main__":
    main()
