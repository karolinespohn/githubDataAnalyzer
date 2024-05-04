import os
from dotenv import load_dotenv
import argparse
import data_query
import data_structuring
import data_analysis


def find_frequent_collaborators(token, owner, repo):
    print("-----------------------------------------------------------------------------------------------------------")
    print("Calculating pair of developers contributing most frequently to the same files measured by number of commits")
    print("-----------------------------------------------------------------------------------------------------------")
    print("Analyzing Data... This may take a while")

    commit_oid_author_files = data_query.fetch_commit_oid_author_files(owner, repo, token)
    file_contributors_map = data_structuring.map_file_to_commits_per_person(commit_oid_author_files)
    max_pairs = data_analysis.get_top_contributor_pair(file_contributors_map)

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

    url_components = repository.split('/')
    try:
        owner = url_components[url_components.index("github.com") + 1]
        repo = url_components[url_components.index("github.com") + 2]
    except IndexError:
        print("URL of repository is invalid")
        return

    find_dev_pair(token, owner, repo)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Find devs contributing most frequently to the same files")
    parser.add_argument("--url", required=True, help="URL of the GitHub repository")

    args = parser.parse_args()
    main(args)
