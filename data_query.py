import requests
from enum import Enum


class Fun(Enum):
    FREQUENT_COLLABORATORS_BY_COMMITS = 1
    FREQUENT_COLLABORATORS_BY_CHANGES = 2
    MOST_CHANGES_PER_COMMIT = 3


def fetch_commit_data(owner, repo, token, queried_data, fun):
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
                        {queried_data}
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

            if data.get("data") and \
                    data.get("data").get("repository").get("defaultBranchRef").get("target") is not None:

                nodes = data.get("data", {}).get("repository", {}).get("defaultBranchRef", {}).\
                    get("target", {}).get("history", {}).get("edges", {})

                match fun:
                    case Fun.FREQUENT_COLLABORATORS_BY_COMMITS | Fun.FREQUENT_COLLABORATORS_BY_CHANGES:
                        for node in nodes:
                            commit_list.extend([(node.get("node").get("oid"),
                                                 node.get("node").get("author").get("name"))])
                    case Fun.MOST_CHANGES_PER_COMMIT:
                        for node in nodes:
                            commit_list.extend([(node.get("node").get("author").get("name"),
                                                 node.get("node").get("additions"),
                                                 node.get("node").get("deletions"))])

                page_info = data.get("data", {}).get("repository", {}).get("defaultBranchRef", {}).\
                    get("target", {}).get("history", {}).get("pageInfo")
                if page_info is None:
                    break

                has_next_page = page_info.get("hasNextPage")
                end_cursor = page_info.get("endCursor")

        else:
            print(f"{response.status_code} Error: {response.text}")
            return []

    return commit_list


def get_corresponding_files(commits, owner, repo, token, fun):
    headers = {
        "Authorization": f"bearer {token}",
    }
    commits_with_files = []

    for commit in commits:
        sha = commit[0]
        committer = commit[1]
        if committer == "GitHub":  # todo: enable option to include commits by github
            continue

        response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}", headers=headers)

        if response.status_code == 200:
            commit_data = response.json()
            files = commit_data.get("files", [])

            match fun:
                case Fun.FREQUENT_COLLABORATORS_BY_COMMITS:
                    for file in files:
                        commits_with_files.append((committer, file["filename"]))
                case Fun.FREQUENT_COLLABORATORS_BY_CHANGES:
                    for file in files:
                        commits_with_files.append((committer, file["filename"], file["changes"]))
        else:
            print(f"{response.status_code} Error: {response.text}")

    return commits_with_files


def fetch_author_files(owner, repo, token):
    queried_data = """oid
                        author {
                            name
                        }"""

    oid_author_list = fetch_commit_data(owner, repo, token, queried_data, Fun.FREQUENT_COLLABORATORS_BY_COMMITS)
    return get_corresponding_files(oid_author_list, owner, repo, token, Fun.FREQUENT_COLLABORATORS_BY_COMMITS)


def fetch_author_files_changes(owner, repo, token):
    queried_data = """oid
                           author {
                               name
                           }"""
    oid_author_changes_list = fetch_commit_data(owner, repo, token, queried_data, Fun.FREQUENT_COLLABORATORS_BY_CHANGES)
    return get_corresponding_files(oid_author_changes_list, owner, repo, token, Fun.FREQUENT_COLLABORATORS_BY_CHANGES)


def fetch_authors_changes(owner, repo, token):
    queried_data = """ additions
                       deletions
                            author {
                                name
                            }"""
    return fetch_commit_data(owner, repo, token, queried_data, Fun.MOST_CHANGES_PER_COMMIT)