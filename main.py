import os
from dotenv import load_dotenv
import argparse
import execute_analysis


def main(args):
    load_dotenv()
    token = os.getenv("GITHUB_API_TOKEN")
    owner, repo, fun = option_parsing(args)

    match fun:
        case "1": execute_analysis.find_frequent_collaborators_by_commits(owner, repo, token)
        case "2": execute_analysis.find_frequent_collaborators_by_changes(owner, repo, token)
        case "3": execute_analysis.find_devs_with_largest_commits(owner, repo, token)
        case "4": execute_analysis.find_devs_with_smallest_commits(owner, repo, token)
        case "5": execute_analysis.find_devs_with_longest_commit_messages(owner, repo, token)
        case _: "Please specify, what kind of analysis you would like to perform"


def option_parsing(args):
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
        if len(repo) > 5 and repo[len(repo) - 4:len(repo)] == ".git":
            repo = repo[0:len(repo) - 4]
        return owner, repo, fun
    except IndexError:
        print("URL of repository is invalid")


if __name__ == '__main__':
    ana_help_string = f"""Specifies which of the following analyses is to be performed:
                      1: Find pair(s) of developers who most frequently commit to the same files
                      2: Find pair(s) of developers who most contribute the largest amount of code to the same files
                      3: Find developer with the largest commits 
                      4: Find developer with the smallest commits
                      5: Find developer with the longest commit messages"""

    parser = argparse.ArgumentParser(description="Find devs contributing most frequently to the same files",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("--url", required=True, help="URL of the GitHub repository")
    parser.add_argument("--ana", required=True, help=ana_help_string)

    main(parser.parse_args())
