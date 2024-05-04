import data_query
import data_structuring
import data_analysis
from utils import Fun


def print_header(description):
    border = len(description) * "-"
    print(border)
    print(description)
    print(border)


def print_dev_pairs(max_pairs):
    if len(max_pairs) == 0:
        print("No pair could be found")
    else:
        print(f"The pair{'s' if len(max_pairs) > 1 else ''} "
              f"of developers contributing most frequently to the same files are:")
        for pair in max_pairs:
            print(f"{pair[0]} & {pair[1]}")


def print_devs_with_extreme_avg(devs, description):
    num_devs_found = len(devs)

    if num_devs_found == 0:
        print("No developer could be found")
    else:
        print(
            f"The developer{'s' if num_devs_found > 1 else ''} "
            f"with the {description} {'are' if num_devs_found > 1 else 'is'}:")
        for dev in devs:
            print(dev)


def get_devs_commit_sizes(owner, repo, token, function):
    author_changes_list = data_query.fetch_authors_changes(owner, repo, token)
    dev_to_changes_map = data_structuring.map_dev_to_avg(author_changes_list, function)
    return data_analysis.get_dev_with_extreme_avg(dev_to_changes_map, function)


def find_frequent_collaborators_by_commits(owner, repo, token):
    print_header("Calculating pair of developers contributing most "
                 "frequently to the same files measured by number of commits")
    print("Fetching data... This may take a while")

    author_files = data_query.fetch_author_files(owner, repo, token)
    file_contributors_map = data_structuring.map_file_to_commits_per_person(author_files)
    max_pairs = data_analysis.get_frequent_collaborators(file_contributors_map)

    print_dev_pairs(max_pairs)


def find_frequent_collaborators_by_changes(owner, repo, token):
    print_header("Calculating pair of developers contributing most "
                 "frequently to the same files measured by changes to file")
    print("Fetching data... This may take a while")

    author_files_changes = data_query.fetch_author_files_changes(owner, repo, token)
    file_contributors_map = data_structuring.map_file_to_changes_per_person(author_files_changes)
    max_pairs = data_analysis.get_frequent_collaborators(file_contributors_map)

    print_dev_pairs(max_pairs)


def find_devs_with_largest_commits(owner, repo, token):
    print_header("Calculating developer with largest commits measured by average changes per commit")

    devs_with_largest_commits = get_devs_commit_sizes(owner, repo, token, Fun.MOST_CHANGES_PER_COMMIT)

    print_devs_with_extreme_avg(devs_with_largest_commits, "largest average commits")


def find_devs_with_smallest_commits(owner, repo, token):
    print_header("Calculating developer with smallest commits measured by average changes per commit")

    devs_with_largest_commits = get_devs_commit_sizes(owner, repo, token, Fun.LEAST_CHANGES_PER_COMMIT)

    print_devs_with_extreme_avg(devs_with_largest_commits, "smallest average commits")


def find_devs_with_longest_commit_messages(owner, repo, token):
    print_header("Calculating developer who on average writes the longest commit messages")
    author_msg_list = data_query.fetch_author_messages(owner, repo, token)
    dev_to_msglen_map = data_structuring.map_dev_to_avg(author_msg_list, Fun.LONGEST_AVG_COMMIT_MESSAGES)
    devs_longest_msgs = data_analysis.get_dev_with_extreme_avg(dev_to_msglen_map, Fun.LONGEST_AVG_COMMIT_MESSAGES)

    print_devs_with_extreme_avg(devs_longest_msgs, "longest average commit messages")

