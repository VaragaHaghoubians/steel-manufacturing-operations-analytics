# Publish manually to GitHub with PowerShell

## 1. Create an empty repository on GitHub

Open https://github.com/new while signed in as **VaragaHaghoubians**. Name the repository
**steel-manufacturing-operations-analytics**. Suggested description:
"Beginner Python project analyzing production, OEE, downtime, scrap and cycle times using synthetic steel manufacturing data."
Choose Public for recruiter visibility. Leave Add README, .gitignore and license unchecked
because this project already includes them. Click Create repository. Copy its HTTPS URL.

Git commands push to an existing remote; they do not create the GitHub repository itself.
This guide deliberately uses the GitHub website for that manual step.

## 2. Extract the downloaded ZIP

Install Git for Windows first if `git --version` is unavailable. Save the ZIP in your
Downloads folder under its supplied name. In a new PowerShell window run:

```powershell
$zipPath = Join-Path $HOME 'Downloads\steel-manufacturing-operations-analytics.zip'
$portfolioFolder = Join-Path $HOME 'Documents\GitHub'
New-Item -ItemType Directory -Path $portfolioFolder -Force | Out-Null
Expand-Archive -LiteralPath $zipPath -DestinationPath $portfolioFolder
Set-Location (Join-Path $portfolioFolder 'steel-manufacturing-operations-analytics')
git --version
```

If the extraction folder already exists, choose another destination; do not overwrite
existing work. If your download location differs, change only `$zipPath`.

## 3. Create the local history and push

The repository URL below uses your account, **VaragaHaghoubians**. Enter your preferred
commit name and GitHub verified or no-reply email when prompted:

```powershell
$githubUser = 'VaragaHaghoubians'
$commitName = Read-Host 'Your name for Git commits'
$commitEmail = Read-Host 'Your GitHub verified or no-reply email'
git init -b main
git config user.name "$commitName"
git config user.email "$commitEmail"
git add .
git status
git commit -m "Add steel manufacturing operations analytics portfolio"
git remote add origin "https://github.com/$githubUser/steel-manufacturing-operations-analytics.git"
git remote -v
git push -u origin main
```

Read `git status` before committing and stop if any command reports an error. The included
.gitignore excludes the environment, credentials and private data.
Git for Windows may open a browser to authenticate. Sign into the account that owns the
repository; your GitHub password is not an HTTPS Git token. Never put a token in these
commands or files. If needed, follow GitHub's authentication guide.

## 4. Confirm and update

```powershell
git status
git log -1 --oneline
Start-Process 'https://github.com/VaragaHaghoubians/steel-manufacturing-operations-analytics'
```
The README, chart previews, notebooks and documents should appear on GitHub.
Later, after reviewing your changes:
```powershell
git add .
git commit -m "Update manufacturing analysis"
git push
```

## Troubleshooting

- Repository not found: confirm the remote URL, browser account and that the empty repository exists.
- `origin` already exists: inspect `git remote -v`; if it is wrong, use
  `git remote set-url origin "https://github.com/$githubUser/steel-manufacturing-operations-analytics.git"`.
- Rejected push / remote already has commits: stop. Do not force-push. Prefer a newly
  created empty repository or review and reconcile the existing history separately.
- Python launcher unavailable: install Python 3.10+; if `python --version` works, use
  `python` in place of `py -3` to create the virtual environment.

References: [official local-code publishing guide](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github),
[remote management](https://docs.github.com/en/get-started/git-basics/managing-remote-repositories).
