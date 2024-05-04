from collections import defaultdict
from utils import Fun


def map_file_to_commits_per_person(commits):
    file_to_contributors_map = defaultdict(lambda: defaultdict(int))
    for committer, file in commits:
        file_to_contributors_map[file][committer] += 1
    return file_to_contributors_map


def map_file_to_changes_per_person(commits):
    file_to_contributors_map = defaultdict(lambda: defaultdict(int))
    for committer, file, changes in commits:
        file_to_contributors_map[file][committer] += changes
    return file_to_contributors_map


def map_dev_to_avg(commits, fun):
    dev_to_avg_map = defaultdict(lambda: [0, 0, 0.0])  # dev -> changes, commits, average
    summand = 0
    for commit in commits: # (name, additions, deletions)
        if fun == Fun.MOST_CHANGES_PER_COMMIT or fun == Fun.LEAST_CHANGES_PER_COMMIT:
            summand = int(commit[1]) + int(commit[2])
        elif fun == Fun.LONGEST_AVG_COMMIT_MESSAGES:
            summand = len(commit[1])

        entry = dev_to_avg_map[commit[0]]
        entry[0] += summand
        entry[1] += 1
        entry[2] = entry[0] / entry[1]

    return dev_to_avg_map

