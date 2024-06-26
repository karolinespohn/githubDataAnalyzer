from enum import Enum


class Fun(Enum):
    FREQUENT_COLLABORATORS_BY_COMMITS = 1
    FREQUENT_COLLABORATORS_BY_CHANGES = 2
    MOST_CHANGES_PER_COMMIT = 3
    LEAST_CHANGES_PER_COMMIT = 4
    LONGEST_AVG_COMMIT_MESSAGES = 5
