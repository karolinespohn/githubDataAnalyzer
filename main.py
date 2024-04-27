import os
import requests
import dotenv

dotenv.load_dotenv()
token = os.getenv("GITHUB_API_TOKEN")


def fetch_commits():
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
                        committer {{
                            name
                        }}
                        file(path:"/") {{
                            object{{
                              ... on Tree{{
                                entries{{
                                  path
                                  type
                                }}
                              }}
                            }}
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

            if data.get("data") and data.get("data").get("repository").get("defaultBranchRef").get(
                    "target") is not None:
                nodes = data.get("data", {}).get("repository", {}).get("defaultBranchRef", {}).get("target", {}).get(
                    "history", {}).get("edges", {})
                commit_list.extend([
                    (
                        node.get("node").get("committer").get("name"),
                        [(entry.get("path"), entry.get("type")) for entry in
                         node.get("node").get("file", {}).get("object", {}).get("entries", [])]
                    )
                    for node in nodes
                ])

                page_info = data.get("data", {}).get("repository", {}).get("defaultBranchRef", {}).get("target", {}).get("history", {}).get("pageInfo")
                if page_info is None:
                    break

                has_next_page = page_info.get("hasNextPage")
                end_cursor = page_info.get("endCursor")

        else:
            print(f"{response.status_code} Error: {response.text}")
            return []

    return commit_list


if __name__ == '__main__':
    repository = "https://github.com/karolinespohn/Notes"
    owner = repository.split("/")[3]
    repo = repository.split("/")[4]
    commits = fetch_commits()
    count = 0
    for commit in commits:
        count += 1
        print(commit)
    print(count)