from collections import defaultdict
from utils import Fun


"""
for each file and pair of contributors a and b, the minimum of commits to that file by either a or b is added to a count
of their shared commits
"""


def get_frequent_collaborators(file_to_committers_map):
    dev_pairs = defaultdict(int)
    max_shared_commits = 0
    max_pairs = []

    for committers in file_to_committers_map.values():
        sorted_committers = sorted(committers.items(), key=lambda x: x[0])

        for i in range(len(sorted_committers)):
            for j in range(i + 1, len(sorted_committers)):
                committer1, committer1_count = sorted_committers[i]
                committer2, committer2_count = sorted_committers[j]

                pair = (committer1, committer2)

                dev_pairs[str(pair)] += min(committer1_count, committer2_count)

                shared_commits = dev_pairs[str(pair)]

                if shared_commits == max_shared_commits:
                    max_pairs.append(pair)

                if shared_commits > max_shared_commits:
                    max_pairs = [pair]
                    max_shared_commits = shared_commits

    return max_pairs


def get_dev_with_avg_changes_extrema(dev_to_changes_map, fun):
    extreme_changes_per_commit = 0
    devs_with_avg_changes_extrema = []

    for dev in dev_to_changes_map:
        data = dev_to_changes_map[dev]
        changes = data[2]
        if int(changes) == extreme_changes_per_commit:
            devs_with_avg_changes_extrema.append(dev)
        if (fun == Fun.MOST_CHANGES_PER_COMMIT and int(changes) > extreme_changes_per_commit) or (fun == Fun.LEAST_CHANGES_PER_COMMIT and (int(changes) < extreme_changes_per_commit or extreme_changes_per_commit == 0)):
            extreme_changes_per_commit = changes
            devs_with_avg_changes_extrema = [dev]

    if extreme_changes_per_commit == 0:
        return None

    return devs_with_avg_changes_extrema
