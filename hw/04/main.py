#!/usr/bin/env python3
import sys


class Solution:
    def __init__(self):
        self.solution = []


def branch_and_bound(processing_times, release_times, deadlines, scheduled_tasks, tasks_to_be_scheduled, best_solution, upper_bound, scheduled_tasks_time=0):
    for j in tasks_to_be_scheduled:
        if max(scheduled_tasks_time, release_times[j]) + processing_times[j] > deadlines[j]:
            return False

    if len(tasks_to_be_scheduled) == 0:
        if upper_bound[0] is None or scheduled_tasks_time < upper_bound[0]:
            upper_bound[0] = scheduled_tasks_time
            best_solution.solution = scheduled_tasks.copy()
        return False
    else:
        lower_bound = max(scheduled_tasks_time, min(release_times[j] for j in tasks_to_be_scheduled)) + sum(processing_times[j] for j in tasks_to_be_scheduled)
        if upper_bound[0] is None:
            temp_upper_bound = max(deadlines[j] for j in tasks_to_be_scheduled)
            if lower_bound > temp_upper_bound:
                return False
        else:
            if lower_bound >= upper_bound[0]:
                return False

    optimal_partial_solution = False
    if min(release_times[j] for j in tasks_to_be_scheduled) >= scheduled_tasks_time:
        best_solution.solution += scheduled_tasks
        optimal_partial_solution = True

    for i in range(len(tasks_to_be_scheduled)):
        if branch_and_bound(processing_times, release_times, deadlines, scheduled_tasks + [tasks_to_be_scheduled[i]], tasks_to_be_scheduled[:i] + tasks_to_be_scheduled[i+1:], best_solution, upper_bound, max(scheduled_tasks_time, release_times[tasks_to_be_scheduled[i]]) + processing_times[tasks_to_be_scheduled[i]]):
            return True
    return optimal_partial_solution


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        number_of_tasks = int(f.readline())
        processing_times = [None for i in range(number_of_tasks)]
        release_times = processing_times.copy()
        deadlines = processing_times.copy()
        for i in range(number_of_tasks):
            processing_times[i], release_times[i], deadlines[i] = [
                int(x) for x in f.readline().split()
            ]
    scheduled_tasks = []
    tasks_to_be_scheduled = [i for i in range(number_of_tasks)]

    best_solution = Solution()
    upper_bound = [None]

    branch_and_bound(processing_times, release_times, deadlines,
                     scheduled_tasks, tasks_to_be_scheduled, best_solution,
                     upper_bound)

    with open(sys.argv[2], "w") as f:
        if len(best_solution.solution) == 0:
            f.write(str(-1) + "\n")
        else:
            c = 0
            schedule = [0 for i in range(number_of_tasks)]
            for i in best_solution.solution:
                scheduled_time = max(c, release_times[i])
                schedule[i] = scheduled_time
                c = scheduled_time + processing_times[i]
            for s in schedule:
                f.write(str(s) + "\n")
