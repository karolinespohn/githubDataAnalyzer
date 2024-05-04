import os
from dotenv import load_dotenv
import argparse
import data_query
import data_structuring
import data_analysis


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
        print(f"The pair(s) of developers contributing most frequently to the same files are:")
        for pair in max_pairs:
            print(f"{pair[0]} & {pair[1]}")


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

    print("reached")
    match fun:
        case "1": find_frequent_collaborators_by_commits(owner, repo, token)
        case "2": find_frequent_collaborators_by_changes(owner, repo, token)
        case _ : "Please specify, what kind of analysis you would like to perform"


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Find devs contributing most frequently to the same files")
    parser.add_argument("--url", required=True, help="URL of the GitHub repository")
    parser.add_argument("--ana", required=True, help="Analysis to be performed")

    args = parser.parse_args()
    main(args)
