How to use this script?

First, update the first 3 variables with what you have:

localFolderPath - a folder on your machine. Use double \\ in path because of escaping
sourceRepoPath - the source git path - in your case AzureDevOps
destinationRepoPath - in your case bitbucket

Notes:
- The folder profided in localFolderPath must exist on disk (preferably C:\tmp or similar)
- The destination repository must be already created on Bitbucket

How to run the script:
python3 syncRepos.py


Notes if problems:
- If the script fails with something like "Host key verification failed", it is because you never trusted the AzureDevOps / Bitbucket ssh fingerprints. For that run some git clone on both, and select "yes" when asked "are you sure you want to trust this"

- If you do not have the setup for git, configure it in file: C:\Users\$your_user\.ssh\config. Add something like:


host azuredevops.com
user git
identityfile C:\Users\path\to\my\key
host bitbucket.com
user git
identityfile C:\Users\path\to\my\other\key
