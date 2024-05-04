from collections import defaultdict


def map_file_to_commits_per_person(commits):
    file_contributors_map = defaultdict(lambda: defaultdict(int))
    for committer, file in commits:
        file_contributors_map[file][committer] += 1
    return file_contributors_map


def map_file_to_changes_per_person(commits):
    file_contributors_map = defaultdict(lambda: defaultdict(int))
    for committer, file, changes in commits:
        file_contributors_map[file][committer] += changes
    return file_contributors_map
