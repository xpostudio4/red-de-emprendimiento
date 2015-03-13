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
#env.hosts = ["45.55.175.61"]
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
    run('git config --global user.name "Leonardo Jimenez"')
    run("sudo apt-get install git")
    run('git config --global user.email ljimenez@stancedata.com')
    run('git commit --amend --reset-author')

def create_repository():
    """
    This function creates the bare repo for the app and  the
    related post hooks.
    """
    hook_text = """#!/bin/sh
GIT_WORK_TREE=/home/django/app/ git checkout -f master
GIT_WORK_TREE=/home/django/app git reset --hard
"""
    #run("mkdir /home/django/app")
    #run("mkdir app_repo.git")
    #with cd("app_repo.git"):
    #    run("git init --bare")
    with cd("~/app_repo.git/hooks"):
        run("touch post-receive")
        run("chmod +x post-receive")
        append('post-receive', hook_text)

def set_local_repo():
    """
    This functions creates the remote for the digital remote locally.
    """
    local("git remote add digital  root@" + env.hosts[0] + ":~/app_repo.git")

def install_nginx():
    """
    This function verifies if nginx is present, if not it install it.
    """
    is_installed = run('nginx -v')
    if is_installed.return_code == 0:
        print("nginx installed already")
    #here should be present and else

def install_gunicorn():
    """
    This function verifies if gunicorn is present, if not it install it.
    """
    is_installed = run('gunicorn -v')
    if is_installed.return_code == 0:
        print("nginx installed already")
    #here should be present and else

def config_nginx():
    """
    This function configure nginx for using our app, also makes a copy of the file
    to avoid spoiling it.
    """
    with cd("/etc/nginx/sites-enabled/"):
        run("cp django django-copy")
        run("sed -i '19s/.*/        alias ~\/home\/django\/app\/media;/' django")
        run("sed -i '24s/.*/        alias ~\/home\/django\/app\/static;/' django")
        run("service restart nginx")

def config_gunicorn():
    """
    This function configure gunicorn for using our app, also makes a copy of the file
    to avoid spoiling it.

    The path for the logs are vim /var/log/nginx/error.log (nginx) and
    vim /var/log/upstart/gunicorn.log (gunicorn)
    """

    with cd("/etc/init/"):
        run("cp gunicorn.conf gunicorn.conf-copy")
        run("sed -i '11s/.*/chdir \/home\/django\/app/' gunicorn.conf")
        run("sed -i '14s/.*/    --name=app \\\\ /' gunicorn.conf")
        run("sed -i '15s/.*/    --pythonpath=app \\\\/ /' gunicorn.conf")
        run("sed -i '18s/.*/    app.wsgi:application/' gunicorn.conf")
        run("service gunicorn restart")

def install_supervisor():
    run("apt-get install supervisor")
    run("vim /var/log/upstart/gunicorn.log")
    # luego se crea el file de configuracion de nginx and gunicorn

