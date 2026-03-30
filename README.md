# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

``A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

###  Smarter Scheduling

Added Filtering for schedule conflitcs of the same date and time that can't be moved around and improved sorting based on time

### Testing PawPal+
test_mark_complete_updates_status checks if complemtion markes complete as true
testing_adding_task_increase_task_count confirms the increase of a pet's task count
test_filter_task_by_completion returns only compelted task when required and only incomplete tasks when requested
test_schedule_tasks_return_chornological_order validates if it sorts by date/time
test_scheduler_detects_duplicate_static_task_times duplicate static task check for   warning
test_detect_static_conflicts_returns_warning checking a warning if the warning actually is shown
test_daily_task_recreates_after_completion Does a daily task create a new task for tomorrow