from fabric.api import run, local, env

env.hosts = ['del.sedamcvrkuta.com']
env.user = 'root'

name = 'seventweets'
host_port = 80
container_port = 8000
repository = 'kedza/sewentweets'
network = 'radionica'


def build(tag=''):
    if tag is not '':
        tag = ':' + tag
    local(f'docker build -t {repository}{tag} .')


def push(tag=''):
    local(f'docker push {repository}{tag}')


def pull(tag=''):
    run(f'docker pull {repository}{tag}')


def create_network():
    run(f'docker network create {network}')


def start(tag=''):
    run(f'''
        docker run -d \
            --name {name} \
            --net {network} \
            -p {host_port}:{container_port} \
            {repository}{tag}
        ''')


def stop():
    run(f'docker stop {name}')
    run(f'docker rm {name}')


def restart():
    stop()
    start()


def deploy(tag=''):
    build(tag)
    push(tag)

    pull()
    stop()
    start()
