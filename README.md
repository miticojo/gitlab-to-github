# Gitlab-to-Github
Utility to migrate all repositories from Gitlab to Github. 

## Note
* skip repository already present on Github
* all repository are created as Private on Github
* no repository will be deleted on Gitlab
* a report of migration is returned at the end of process to check what's goes wrong

## Requirements
* gitlab credentials and token 
* ssh keys shared on github
* github user token
* python libs python-gitlab and pygithub
* git client installed

## Install 
``` bash
git clone https://github.com/miticojo/gitlab-to-github.git
cd gitlab-to-github
sudo pip istall -r requirements
```
## Run
set your credentials in migrate.py
``` bash
gitlab_cred = { 
   'user': 'xxxxxxx',
   'pass': 'xxxxxxxx',
   'token': 'xxxxxxxxxxxxxxxx',
   'host': 'https://gitlab.xxxxxxxxxxx.com'
}
github_cred = {
   'token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxx',
}
``` 
and run it:
``` bash
# start repo migration
python migrate.py
```
