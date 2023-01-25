# !pip install gitpython 
import git

# Initialize the repository object
repo_path = 'C:\DevSoft\PyDev\Dev2023\python_automation'
repo = git.Repo(repo_path)

# Stage all changes
repo.git.add('--all')

# Commit the changes with a message
repo.index.commit('Commit message')

# Push the changes to GitHub
origin = repo.remote(name='origin')
origin.push()