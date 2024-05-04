import os
from dotenv import load_dotenv
import argparse
import data_query
import data_structuring
import data_analysis


# todo: expand this to return a list, in order to handle multiple pairs with same amount of commits
def find_dev_pair(token, owner, repo):
    print("Calculating pair of developers contributing most frequently to the same files measured by number of commits")
    print("Analyzing Data... This may take a while")

    commit_oid_author_files = data_query.fetch_commit_oid_author_files(owner, repo, token)
    file_contributors_map = data_structuring.map_file_to_commits_per_person(commit_oid_author_files)
    max_pair = data_analysis.get_top_contributor_pair(file_contributors_map)

    if None in max_pair:
        print("No pair could be found")
    else:
        print(f"The two developers contributing most frequently to the same files are {max_pair[0]} and {max_pair[1]}")


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
