import os
import requests
from dotenv import load_dotenv
from collections import defaultdict
import argparse


def fetch_commits(owner, repo, token):
    has_next_page = True  # in one query, graphql only returns 100 commits at most, this ensures flipping through pages
    end_cursor = None
    commit_list = []

    headers = {
        "Authorization": f"bearer {token}",
        "Content-Type": "application/json"
    }





















    while has_next_page:
        cursor = f', after: "{end_cursor}"' if end_cursor else ''
        query = f"""
        query {{
          repository(owner: "{owner}", name: "{repo}") {{
            defaultBranchRef {{
              target {{
                ... on Commit {{
                  history(first: 100{cursor}) {{
                    pageInfo {{
                          hasNextPage
                          endCursor
                        }}
                    edges {{
                      node {{
                        oid
                        committer {{
                            name
                        }}
                      }}
                    }}
                  }}
                }}
              }}
            }}
          }}
        }}
        """
        response = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)

        if response.status_code == 200:
            data = response.json()

            if data.get("data") and data.get("data").get("repository").get("defaultBranchRef").get("target") is not None:

                nodes = data.get("data", {}).get("repository", {}).get("defaultBranchRef", {}).get("target", {}).get("history", {}).get("edges", {})

                for node in nodes:
                    commit_list.extend([(node.get("node").get("oid"), node.get("node").get("committer").get("name"))])


                page_info = data.get("data", {}).get("repository", {}).get("defaultBranchRef", {}).get("target", {}).get("history", {}).get("pageInfo")
                if page_info is None:
                    break

                has_next_page = page_info.get("hasNextPage")
                end_cursor = page_info.get("endCursor")

        else:
            print(f"{response.status_code} Error: {response.text}")
            return []

    return commit_list


def get_corresponding_files(commits, owner, repo, token):
    headers = {
        "Authorization": f"bearer {token}",
    }
    committer_file_list = []

    for (sha, committer) in commits:
        if committer == "GitHub": # todo: enable option to include commits by github
            continue

        response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}", headers=headers)

        if response.status_code == 200:
            commit_data = response.json()
            files = commit_data.get("files", [])

            for file in files:
                committer_file_list.append((committer, file["filename"]))
        else:
            print(f"{response.status_code} Error: {response.text}")

    return committer_file_list


def set_up_map(commits):
    file_contributors_map = defaultdict(lambda: defaultdict(int))
    for committer, file in commits:
        file_contributors_map[file][committer] += 1
    return file_contributors_map


"""
for each file and pair of contributors a and b, the minimum of commits to that file by either a or b is added to a count
of their shared commits
"""
def get_max_pair(file_to_committers_map):
    dev_pairs = defaultdict(int)
    max_shared_commits = 0
    max_pair = (None, None)

    for committers in file_to_committers_map.values():
        sorted_committers = sorted(committers.items(), key=lambda x: x[0])

        for i in range(len(sorted_committers)):
            for j in range (i + 1, len(sorted_committers)):
                committer1, committer1_count = sorted_committers[i]
                committer2, committer2_count = sorted_committers[j]

                pair = (committer1, committer2)

                dev_pairs[str(pair)] += min(committer1_count, committer2_count)

                shared_commits = dev_pairs[str(pair)]

                if shared_commits > max_shared_commits:
                    max_pair = pair
                    max_shared_commits = shared_commits

    return max_pair


def find_dev_pair(token, owner, repo):
    print("Analyzing Data... This may take a while")
    commits = fetch_commits(owner, repo, token)

    committer_file_list = get_corresponding_files(commits, owner, repo, token)

    file_contributors_map = set_up_map(committer_file_list)
    max_pair = get_max_pair(file_contributors_map)

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

    urlComponents = repository.split('/')
    try:
        owner = urlComponents[urlComponents.index("github.com") + 1]
        repo = urlComponents[urlComponents.index("github.com") + 2]
    except IndexError:
        print("URL of repository is invalid")
        return



    find_dev_pair(token, owner, repo)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Find devs contributing most frequently to the same files")
    parser.add_argument("--url", required=True, help="URL of the GitHub repository")

    args = parser.parse_args()
    main(args)

