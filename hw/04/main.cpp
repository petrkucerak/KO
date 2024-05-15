#include <algorithm>
#include <climits>
#include <fstream>
#include <iostream>
#include <vector>

using namespace std;

#define TASK tasks[depth]

struct Task {
   int task_id;
   int process_time;
   int release_time;
   int deadline;
};

bool compareTasks(const Task &task1, const Task &task2)
{
   // First, compare by deadline
   if (task1.deadline < task2.deadline) {
      return true;
   } else if (task1.deadline > task2.deadline) {
      return false;
   } else {
      // If deadline is the same, compare by release_time
      return task1.release_time < task2.release_time;
   }
}

bool catchDeadline(vector<Task> tasks, int start_time, int depth)
{
   while (depth < tasks.size()) {
      if (TASK.process_time + start_time > TASK.deadline)
         return false;
      ++depth;
   }
   return true;
}

bool isReleaseLater(vector<Task> &tasks, int start_time, int depth)
{
   while (depth < tasks.size()) {
      if (TASK.release_time < start_time)
         return false;
      ++depth;
   }
   return true;
}

bool bratleyAlgorithm(vector<Task> &tasks, vector<int> &order, int start_time,
                      int depth, int &best_time, vector<int> &best_order)
{
   bool skip_parents = false;
   if (depth == tasks.size()) {
      if (start_time < best_time) {
         best_time = start_time;
         best_order = order;
      }
      return skip_parents;
   }

   // 1. CONDITION: Missing deadline
   if (!catchDeadline(tasks, start_time, depth)) {
      // cout << "Missing deadline" << endl;
      return skip_parents;
   }
   // 2. CONDITION: Bound on the solution, inspiration by Petr
   int count_process_time = 0;
   int sooner_release_time = 0;
   int best_release_time = 0;
   int peters_magic = 0;
   int history_sum = 0;

   for (int i = depth; i < tasks.size(); ++i) {
      peters_magic += tasks[i].process_time;

      if (tasks[i].release_time > start_time) {
         peters_magic +=
             tasks[i].release_time - start_time - count_process_time;
      } else {
         history_sum += tasks[i].process_time;
      }

      count_process_time += tasks[i].process_time;
      sooner_release_time = min(sooner_release_time, tasks[i].release_time);
      best_release_time = max(best_release_time, tasks[i].release_time);
   }

   int current_time = max(start_time, sooner_release_time);
   if (current_time + count_process_time >= best_time) {
      return skip_parents;
   }

   // CONDITION: Decomposition
   if (sooner_release_time >= start_time) {
      skip_parents = true;
   }

   // // Peter's smart heuristic
   // if (history_sum < best_release_time - start_time &&
   //     start_time + peters_magic >= best_time) {
   //    return skip_parents;
   // }

   bool is_best_tmp = false;
   for (int i = depth; i < tasks.size(); ++i) {
      // swap
      swap(tasks[depth], tasks[i]);

      order[TASK.task_id] = start_time;

      // get end time
      const int end_time =
          max(TASK.release_time, start_time) + TASK.process_time;

      // run the new step of bratley algorithm
      skip_parents = bratleyAlgorithm(tasks, order, end_time, depth + 1,
                                      best_time, best_order);

      // swap back
      swap(tasks[i], tasks[depth]);
      if (skip_parents) {
         return skip_parents;
      }
   }
   return skip_parents;
}

int main(int argc, char **argv)
{

   // Open the file
   ifstream inputFile(argv[1]);
   if (!inputFile.is_open()) {
      fprintf(stderr, "Error opening the file: %s\n", argv[1]);
      return 1;
   }

   int task_count;
   if (!(inputFile >> task_count)) {
      fprintf(stderr, "Can't load the task count from file.\n");
      return 1;
   }

   vector<Task> tasks;
   vector<int> order(task_count);
   tasks.reserve(task_count);
   int best_time = INT_MAX;

   // Open the output file
   ofstream outputFile(argv[2]);
   if (!outputFile.is_open()) {
      fprintf(stderr, "Error opening the output file: %s\n", argv[2]);
      return 1;
   }

   // Load the data from the file
   for (int i = 0; i < task_count; ++i) {
      int process_time, release_time, deadline;
      if (!(inputFile >> process_time >> release_time >> deadline)) {
         fprintf(stderr, "Can't load a task from file.\n");
         return 1;
      }
      // if deadline - process_time < release_time cause error
      if (process_time + release_time > deadline) {
         outputFile << "-1" << endl;
         cout << "-1" << endl;
         return 0;
      }
      tasks.push_back({i, process_time, release_time, deadline});
   }

   // Sort tasks based on release times
   sort(tasks.begin(), tasks.end(), compareTasks);

   vector<int> best_order;

   bratleyAlgorithm(tasks, order, 0, 0, best_time, best_order);
   if (!best_order.empty()) {
      for (auto &task : best_order)
         outputFile << task << endl;
      for (auto &task : best_order)
         cout << task << endl;
   } else {
      outputFile << "-1" << endl;
      cout << "-1" << endl;
   }
   return 0;
}