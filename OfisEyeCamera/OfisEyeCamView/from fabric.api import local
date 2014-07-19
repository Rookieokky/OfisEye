from fabric.api import local
from fabric.api import lcd

def prepare_deployment(OfisEye-dev)
	local('python manage.py test OfisEyeCamView')
	local('git add -p && git commit')
	local('git checkout master && git merge ' + OfisEye-dev)

def deploy():
	with lcd('/OfisEye'):
		local('.git pull /Desktop/OfisEye-dev')
		local('python manage.py test OfisEyeCamView')