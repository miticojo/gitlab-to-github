#!/usr/bin/env python

__author__ = "Giorgio Crivellari"
__copyright__ = "Copyright 2016, Giorgio Crivellari"
__license__ = "GPL"
__version__ = "1.0.0"
__maintainer__ = "Giorgio Crivellari"
__email__ = "miticojo[at]gmail.com"

import os
import shutil
import gitlab
from github import Github

gitlab_cred = { 
   'user': 'xxxxxxx',
   'pass': 'xxxxxxxx',
   'token': 'xxxxxxxxxxxxxxxx',
   'host': 'https://gitlab.xxxxxxxxxxx.com'
}
github_cred = {
   'token': 'xxxxxxxxxxxxxxxxxxxxxxxxxxx',
}

def gitclone(path, url):
   repo_dir = os.path.join(".", path)
   if os.path.isdir(repo_dir): 
	shutil.rmtree(repo_dir)       
   if os.system("git clone --mirror {} {} > /dev/null 2>&1".format(url, repo_dir)) != 0:
      return False
   return True

def gitpush(path, url):
   repo_dir = os.path.join(".", path)
   os.chdir(repo_dir)
   if os.system("git push --no-verify --mirror {}  > /dev/null 2>&1".format(url)) != 0:
      return False
   return True

gitlab = gitlab.Gitlab(gitlab_cred["host"], token=gitlab_cred["token"])
g = Github(github_cred["token"])
g_user = g.get_user()

total=[]
migrated=[]
skipped=[]
failed=[]

for project in gitlab.getall(gitlab.getprojects):
    http_url_to_repo = project["http_url_to_repo"].split("://")
    path = project["path"].lower()
    description = project["description"] 
    total.append(path)
    try:
      if g_user.get_repo(path):
        print "WARN: Repository {} already present on Gihub".format(path)
	skipped.append(path)
        continue
    except: pass
    
    print "INFO: Cloning repo {}".format(path)
    if  not gitclone(path, "{}://{}:{}@{}".format(http_url_to_repo[0], gitlab_cred["user"], gitlab_cred["pass"], http_url_to_repo[1])): 
       print "ERR: Failed during cloning {}".format(path)
       failed.append(path)
       continue
    
    print "INFO: Creating new repo {} on github".format(path)
    try:
       g_repo = g_user.create_repo(path, description=description, private=True)
    except Exception, ex: 
       print "ERR: Failed during creation of repo {} in github: {}".format(path, ex.message)
       failed.append(path)
       continue

    print "INFO: Pushing repo {} on github".format(path)
    if not  gitpush(path, g_repo.ssh_url):
       print "ERR: Failed pushing {} on github".format(path)
       failed.append(path)
       continue

print "#########################"
print "### Migration Summary ###"
print "#########################"
print "Total repo: {}".format(len(total))
print "Skipped repo: {}".format(len(skipped))
print "Failed repo {}: ".format(len(failed))
for r in failed: print "> {}".format(r)
print "#########################"
