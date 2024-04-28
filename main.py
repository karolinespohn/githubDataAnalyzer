import os
import requests
import dotenv


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
        response = requests.get(f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}", headers=headers)

        if response.status_code == 200:
            commit_data = response.json()
            files = commit_data.get("files", [])

            for file in files:
                committer_file_list.append((committer, file["filename"]))
        else:
            print(f"{response.status_code} Error: {response.text}")

    return committer_file_list


if __name__ == '__main__':
    dotenv.load_dotenv()
    token = os.getenv("GITHUB_API_TOKEN")

    repository = "https://github.com/karolinespohn/Notes"
    owner = repository.split("/")[3]
    repo = repository.split("/")[4]

    commits = fetch_commits(owner, repo, token)
    committer_file_list = get_corresponding_files(commits, owner, repo, token)
    print(committer_file_list)


