from collections import defaultdict


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


def map_dev_to_changes(commits):
    dev_to_changes_map = defaultdict(lambda: [0, 0, 0])  # dev -> changes, commits, average
    for commit in commits: # (name, additions, deletions)
        changes = commit[1] + commit[2]

        entry = dev_to_changes_map[commit[0]]
        entry[0] = entry[0] + changes
        entry[1] = entry[1] + 1
        entry[2] = entry[0] / entry[1]

    return dev_to_changes_map


