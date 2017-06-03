from fabric.api import run, local, env, settings

env.hosts = ['del.sedamcvrkuta.com:22202']
env.user = 'root'

service_image = 'kedza/seventweets'
service_container_name = 'seventweets'
service_port = 8000
host_port = 80

network = 'radionica'

db_image_name = 'postgres:9.6.2'
db_container_name = 'radionica-postgres'
db_user = 'radionica'
db_host = '127.0.0.1'
db_port = 5432
db_name = 'radionica'
db_volume = 'radionica-postgres-data'
db_data_path = '/var/lib/postgresql/data'


def build_image():
    local(f'docker build -t {service_image} . --build-arg PORT={service_port}')


def push_image():
    local(f'docker push {service_image}')


def pull_image():
    run(f'docker pull {service_image}')


def create_network():
    with settings(warn_only=True):
        run(f'docker network create {network}')


def start_service(db_pass=None):
    run(f'docker run -d '
        f'--name {service_container_name} '
        f'--net {network} '
        f'-e SEVENTWEETS_DB_USER={db_user} '
        f'-e SEVENTWEETS_DB_PASS={db_pass} '
        f'-e SEVENTWEETS_DB_HOST={db_container_name} '
        f'-e SEVENTWEETS_DB_NAME={db_name} '
        f'-e SEVENTWEETS_DB_PORT={db_port} ' 
        f'-p {host_port}:{service_port} '
        f'{service_image}')


def stop_service():
    with settings(warn_only=True):
        run(f'docker stop {service_container_name}')
        run(f'docker rm {service_container_name}')


def restart_service(db_pass=None):
    stop_service()
    start_service(db_pass)


def create_db_volume():
    with settings(warn_only=True):
        run(f'docker volume create {db_volume}')


def start_db(db_pass=None):
    with settings(warn_only=True):
        run(f'docker run -d '
            f'--name {db_container_name} '
            f'--net {network} '
            f'--restart unless-stopped '
            f'-e POSTGRES_USER={db_user} '
            f'-e POSTGRES_PASSWORD={db_pass} '
            f'-e POSTGRES_DB={db_name} '
            f'-v {db_volume}:{db_data_path} '
            f'-p {db_host}:{db_port}:{db_port} '
            f'{db_image_name}')


def stop_db():
    with settings(warn_only=True):
        run(f'docker stop {db_container_name}')
        run(f'docker rm {db_container_name}')


def migrate_db(db_pass):
    run(f'docker run '
        f'--rm '
        f'--net {network} '
        f'-e SEVENTWEETS_DB_USER={db_user} '
        f'-e SEVENTWEETS_DB_PASS={db_pass} '
        f'-e SEVENTWEETS_DB_HOST={db_container_name} '
        f'-e SEVENTWEETS_DB_NAME={db_name} '
        f'{service_image} '
        'python3 -m migrations')


def deploy(db_pass=None):
    build_image()
    push_image()
    pull_image()

    create_network()
    create_db_volume()

    stop_service()
    start_db(db_pass)
    migrate_db(db_pass)
    start_service(db_pass)


