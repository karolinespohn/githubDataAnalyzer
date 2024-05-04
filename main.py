import os
from dotenv import load_dotenv
import argparse
import data_query
import data_structuring
import data_analysis
from utils import Fun


def find_frequent_collaborators_by_commits(owner, repo, token):
    print("-----------------------------------------------------------------------------------------------------------")
    print("Calculating pair of developers contributing most frequently to the same files measured by number of commits")
    print("-----------------------------------------------------------------------------------------------------------")
    print("Analyzing Data... This may take a while")

    author_files = data_query.fetch_author_files(owner, repo, token)
    file_contributors_map = data_structuring.map_file_to_commits_per_person(author_files)
    max_pairs = data_analysis.get_frequent_collaborators(file_contributors_map)

    if len(max_pairs) == 0:
        print("No pair could be found")
    else:
        print(f"The pair(s) of developers contributing most frequently to the same files are:")
        for pair in max_pairs:
            print(f"{pair[0]} & {pair[1]}")


def find_frequent_collaborators_by_changes(owner, repo, token):
    print("---------------------------------------------------------------------------------------------------------")
    print("Calculating pair of developers contributing most frequently to the same files measured by changes to file")
    print("---------------------------------------------------------------------------------------------------------")
    print("Analyzing Data... This may take a while")
    author_files_changes = data_query.fetch_author_files_changes(owner, repo, token)
    file_contributors_map = data_structuring.map_file_to_changes_per_person(author_files_changes)
    max_pairs = data_analysis.get_frequent_collaborators(file_contributors_map)
    if len(max_pairs) == 0:
        print("No pair could be found")
    else:
        print("The pair(s) of developers contributing most frequently to the same files are:")
        for pair in max_pairs:
            print(f"{pair[0]} & {pair[1]}")


def find_devs_with_largest_commits(owner, repo, token):
    print("---------------------------------------------------------------------------------")
    print("Calculating developer with largest commits measured by average changes per commit")
    print("---------------------------------------------------------------------------------")

    author_changes_list = data_query.fetch_authors_changes(owner, repo, token)
    dev_to_changes_map = data_structuring.map_dev_to_avg(author_changes_list, Fun.MOST_CHANGES_PER_COMMIT)
    devs_with_largest_commits = data_analysis.get_dev_with_extreme_avg(dev_to_changes_map, Fun.MOST_CHANGES_PER_COMMIT)

    num_devs_found = len(devs_with_largest_commits)

    if num_devs_found == 0:
        print("No developer could be found")
    else:
        print(f"The dev{'s' if num_devs_found > 1 else ''} with the largest commits {'are' if num_devs_found > 1 else 'is'}:")
        for dev in devs_with_largest_commits:
            print(dev)


def find_devs_with_smallest_commits(owner, repo, token):
    print("----------------------------------------------------------------------------------")
    print("Calculating developer with smallest commits measured by average changes per commit")
    print("----------------------------------------------------------------------------------")

    author_changes_list = data_query.fetch_authors_changes(owner, repo, token)
    dev_to_changes_map = data_structuring.map_dev_to_avg(author_changes_list, Fun.LEAST_CHANGES_PER_COMMIT)
    devs_with_smallest_commits = data_analysis.get_dev_with_extreme_avg(dev_to_changes_map,
                                                                        Fun.LEAST_CHANGES_PER_COMMIT)

    num_devs_found = len(devs_with_smallest_commits)

    if num_devs_found == 0:
        print("No developer could be found")
    else:
        print(
            f"The dev{'s' if num_devs_found > 1 else ''} with the smallest commits {'are' if num_devs_found > 1 else 'is'}:")
        for dev in devs_with_smallest_commits:
            print(dev)


def find_devs_with_longest_commit_msgs(owner, repo, token):
    print("-----------------------------------------------------------------------")
    print("Calculating developer who on average writes the longest commit messages")
    print("-----------------------------------------------------------------------")

    author_msg_list = data_query.fetch_author_messages(owner, repo, token)
    dev_to_msglen_map = data_structuring.map_dev_to_avg(author_msg_list, Fun.LONGEST_AVG_COMMIT_MESSAGES)
    devs_shortest_msgs = data_analysis.get_dev_with_extreme_avg(dev_to_msglen_map,
                                                                        Fun.LONGEST_AVG_COMMIT_MESSAGES)

    num_devs_found = len(devs_shortest_msgs)

    if num_devs_found == 0:
        print("No developer could be found")
    else:
        print(
            f"The dev{'s' if num_devs_found > 1 else ''} with the longest commit messages {'are' if num_devs_found > 1 else 'is'}:")
        for dev in devs_shortest_msgs:
            print(dev)


def main(args):
    load_dotenv()
    token = os.getenv("GITHUB_API_TOKEN")

    repository = args.url
    if "github.com/" not in repository:
        print("URL of repository is invalid")
        return

    fun = args.ana
    if not fun:
        print("Please specify which analysis you want to perform")

    url_components = repository.split('/')
    try:
        owner = url_components[url_components.index("github.com") + 1]
        repo = url_components[url_components.index("github.com") + 2]
    except IndexError:
        print("URL of repository is invalid")
        return

    match fun:
        case "1": find_frequent_collaborators_by_commits(owner, repo, token)
        case "2": find_frequent_collaborators_by_changes(owner, repo, token)
        case "3": find_devs_with_largest_commits(owner, repo, token)
        case "4": find_devs_with_smallest_commits(owner, repo, token)
        case _: "Please specify, what kind of analysis you would like to perform"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Find devs contributing most frequently to the same files")
    parser.add_argument("--url", required=True, help="URL of the GitHub repository")
    parser.add_argument("--ana", required=True, help="Analysis to be performed")

    args = parser.parse_args()
    main(args)
