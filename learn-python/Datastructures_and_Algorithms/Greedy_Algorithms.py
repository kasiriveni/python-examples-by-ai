# Greedy Algorithms

# Activity Selection Problem
def activity_selection(activities):
    activities.sort(key=lambda x: x[1])
    selected = [activities[0]]
    for i in range(1, len(activities)):
        if activities[i][0] >= selected[-1][1]:
            selected.append(activities[i])
    return selected

activities = [(1, 3), (2, 5), (0, 6), (8, 9), (5, 7), (5, 9)]
print("Selected Activities:", activity_selection(activities))
