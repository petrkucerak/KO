#!/usr/bin/env python3
import sys

class Schedule:
    def __init__(self):
        self.solution = []


def branch_and_bound(processing_times, release_times, deadlines, scheduled_tasks, tasks_to_be_scheduled, best_schedule, upper_bound, scheduled_tasks_time=0):
    # Check if any task cannot be scheduled within its deadline
    for j in tasks_to_be_scheduled:
        if max(scheduled_tasks_time, release_times[j]) + processing_times[j] > deadlines[j]:
            return False

    # If no tasks left to schedule, update best solution if current one is better
    if not tasks_to_be_scheduled:
        if upper_bound[0] is None or scheduled_tasks_time < upper_bound[0]:
            upper_bound[0] = scheduled_tasks_time
            best_schedule.solution = scheduled_tasks.copy()
        return False

    # Calculate lower bound for the current partial solution
    lower_bound = max(scheduled_tasks_time, min(
        release_times[j] for j in tasks_to_be_scheduled)) + sum(processing_times[j] for j in tasks_to_be_scheduled)
    if upper_bound[0] is None:
        temp_upper_bound = max(deadlines[j] for j in tasks_to_be_scheduled)
        if lower_bound > temp_upper_bound:
            return False
    else:
        if lower_bound >= upper_bound[0]:
            return False

    # Check for optimal partial solution
    optimal_partial_solution = False
    if min(release_times[j] for j in tasks_to_be_scheduled) >= scheduled_tasks_time:
        best_schedule.solution += scheduled_tasks
        optimal_partial_solution = True

    # Explore further branching
    for i, task in enumerate(tasks_to_be_scheduled):
        next_task = tasks_to_be_scheduled[i]
        next_scheduled_time = max(
            scheduled_tasks_time, release_times[next_task]) + processing_times[next_task]
        if branch_and_bound(processing_times, release_times, deadlines,
                            scheduled_tasks + [next_task],
                            tasks_to_be_scheduled[:i] +
                            tasks_to_be_scheduled[i+1:],
                            best_schedule, upper_bound, next_scheduled_time):
            return True
    return optimal_partial_solution


if __name__ == "__main__":
    # Read input file
    with open(sys.argv[1]) as f:
        number_of_tasks = int(f.readline().strip())
        processing_times, release_times, deadlines = [], [], []
        for _ in range(number_of_tasks):
            p, r, d = map(int, f.readline().strip().split())
            processing_times.append(p)
            deadlines.append(d)
            release_times.append(r)

    upper_bound = [None]
    best_schedule = Schedule()
    tasks_to_be_scheduled = list(range(number_of_tasks))
    scheduled_tasks = []

    # Execute branch and bound algorithm
    branch_and_bound(processing_times, release_times, deadlines,
                     scheduled_tasks, tasks_to_be_scheduled, best_schedule,
                     upper_bound)

    # Write output file
    with open(sys.argv[2], "w") as f:
        if not best_schedule.solution:
            f.write("-1\n")
        else:
            c = 0
            schedule = [0] * number_of_tasks
            for i in best_schedule.solution:
                scheduled_time = max(c, release_times[i])
                schedule[i] = scheduled_time
                c = scheduled_time + processing_times[i]
            for s in schedule:
                f.write(f"{s}\n")
