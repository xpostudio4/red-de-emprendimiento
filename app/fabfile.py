"""
   The purpose of this script is to handle the upload of the app to the server
   this include the setup of the server, installation of git, nginx, gunicorn
   supervisor and all the required libraries for the well functioning of the
   site.

   For this purpose we plan on using  two simple API's fabric for task
   automation and poseidon for automation of certain task within digitalocean.
"""
from fabric.api import abort, cd, local, settings, run, env
from fabric.contrib.files import append
#configuration
env.use_ssh_config = True
env.user = "root"
env.hosts = ["104.236.29.231"]
env.key_filename = "/Users/leonardojimenez/.ssh/id_rsa"
env.password = "Jesusvictor1"

#env.ssh_config_path = "/Users/leonardojimenez/.ssh/known_hosts"

#import poseidon.api as po
def deploy():
    """
        The purpose of this function is to be the one conecting to the remote
        digitalocean servers and install all the basic issues needed to work
         - Git.
    """
    run("cd /home/")
    install_git()
    #create repository
    #install nginx
    #install gunicorn
    #install supervisor
    #configure nginx
    #configure gunicorn
    #configure supervisor
    #set digital_remote locally
    #push

def install_git():
    """Install git in a Ubuntu instance in digital ocean"""
    print("installing updates for the system...")
    run("sudo apt-get update")
    print("installing last version of git...")
    run("sudo apt-get install git")
    run('git config --global user.name "Leonardo Jimenez"')
    run('git config --global user.email ljimenez@stancedata.com')
    run('git commit --amend --reset-author')

def create_repository():
    """
    This function creates the bare repo for the app and  the
    related post hooks.
    """
    hook_text = """#!/bin/sh
GIT_WORK_TREE=~/app/ git checkout -f master
GIT_WORK_TREE=~/app/ git reset --hard
"""
    run("mkdir ~/app")
    run("mkdir app_repo.git")
    with cd("app_repo.git"):
        run("git init --bare")
    with cd("~/app_repo.git/hooks"):
        run("touch post-receive")
        append('post-receive', hook_text)

def set_local_repo():
    """
    This functions creates the remote for the digital remote locally.
    """
    local("git remote add digital  root@" + env.hosts[0] + ":~/app_repo.git")

