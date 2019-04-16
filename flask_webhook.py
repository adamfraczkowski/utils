from bottle import route,request,run,HTTPResponse
import subprocess
import threading

HEADER_NAME = "X-Gitlab-Token"
KEY=""
WORK_DIR=""
COMPOSE_FILE_NAME="docker-compose.deploy.yml"


def git_pull():
    subprocess.call(['git','pull'],cwd=WORK_DIR,stdout=subprocess.PIPE)
    subprocess.call(['git','checkout','deploy'],cwd=WORK_DIR,stdout=subprocess.PIPE)
    #result = result.communicate()[0]
    return 0

def compose_restart():
    subprocess.call(['docker-compose','restart'],cwd=WORK_DIR,stdout=subprocess.PIPE)
    subprocess.call(['docker-compose','up','-d','--build'],cwd=WORK_DIR,stdout=subprocess.PIPE)
    return 0

def make_migration():
    subprocess.call(['docker-compose','run','web','python3','manage.py','migrate'],cwd=WORK_DIR,stdout=subprocess.PIPE)

def make_deploy():
    git_pull()
    compose_restart()
    make_migration()

@route('/deploy')
@route('/deploy',method="POST")
def index():
    header_key = request.get_header(HEADER_NAME)
    if header_key == KEY:
        thread = threading.Thread(target=make_deploy,args=())
        thread.daemon = True
        thread.start()
        return HTTPResponse("OK",200)
    else:
        return HTTPResponse("UNAUTHORIZED",401)
        



run(host='0.0.0.0', port=9092)

