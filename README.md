# Description
This is a CLI tool to analyze data from github repositories.
## Possible Analyses
- 1: Find the pair(s) of developers most frequently commit to the same repos
- 2: Find pair(s) of developers who contribute the largest amount of code to the same files 
- 3: Find developer with the largest commits 
- 4: Find developer with the smallest commits 
- 5: Find developer with the longest commit messages
# Build Instructions
- paste your api key into a .env file
- execute the following commands:
```
pip install -r requirements.txt
python3 main.py —url <repo_url> —ana <type_of_analysis_to_perform>
```

Have fun!
