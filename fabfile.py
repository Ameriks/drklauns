from fabric.api import run, env, hosts, sudo, cd, task, local
from fabric.tasks import Task

env.hosts = ['newdocker', ]
env.use_ssh_config = True


@task
def rebuild_docker():
    local("docker-compose build projectdrklauns")
    local("docker-compose -f dev.yml build django")
    local("docker push ameriks/project_drklauns:latest")


class Deploy(Task):
    name = "deploy"
    docker_id = None
    need_static_regenerate = False
    need_migrate = False
    need_service_restart = False
    need_full_restart = False

    def get_project_id(self):
        self.docker_id = run('docker ps | grep "citdnew_projectdrklauns_1" | cut -c1-12')

    def collect_static(self):
        run("docker exec %s /app/manage.py collectstatic --no-input" % self.docker_id)
        self.need_static_regenerate = False

    def restart_services(self):
        run("docker exec %s kill -HUP 1" % self.docker_id)

    def migrate(self):
        run("docker exec %s /app/manage.py migrate" % self.docker_id)
        self.need_migrate = False

    def git_pull(self):
        git_output = run("docker exec %s git pull" % self.docker_id)
        if "static/" in git_output or 'requirements/' in git_output:
            self.need_static_regenerate = True

        if "migrations/" in git_output:
            self.need_migrate = True

        if ".py" in git_output or ".html" in git_output:
            self.need_service_restart = True

    def pull_docker(self):
        pull_result = run("docker pull ameriks/project_drklauns:latest")
        if 'Image is up to date' not in pull_result:
            self.need_full_restart = True

    def restart_docker_compose(self):
        with cd('/var/lib/app/project_drklauns'):
            run("docker-compose -p citdnew up -d -t 30 projectdrklauns")

    def run(self):
        self.get_project_id()
        self.git_pull()
        if self.need_migrate:
            self.migrate()

        if self.need_static_regenerate:
            self.collect_static()

        self.pull_docker()

        if not self.need_full_restart and self.need_service_restart:
            self.restart_services()
        elif self.need_full_restart:
            self.restart_docker_compose()
instance = Deploy()
