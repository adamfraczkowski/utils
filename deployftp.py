#Author AdamFraczkowski
import subprocess
from git import Repo
from ftplib import FTP, error_perm
import os

ftpHandler = FTP()

# OPTIONS TO CHANGE
GIT_DEPLOY_BRANCH = 'master'
GIT_REMOTE_NAME = 'origin'
IGNORE_FILE = '.ftpignore'
SOURCE_DIR = '.'
FTP_SOURCE_DIR = 'deploy'

FTP_SERVER = '127.0.0.1'
FTP_PORT = 21
FTP_USERNAME = ''
FTP_PASSWORD = ''
# ------------------
gitrepo = Repo(SOURCE_DIR)

ftpHandler.connect(FTP_SERVER,FTP_PORT)
ftpHandler.login(FTP_USERNAME,FTP_PASSWORD)

def before_transfer():
    subprocess.call([GIT_PATH,'checkout',GIT_DEPLOY_BRANCH],cwd=SOURCE_DIR)

def git_file_list():
    FILE_LISTING = {
        "M":[],
        "A":[],
        "D":[]
    }
    result = gitrepo.index.diff(GIT_REMOTE_NAME+'/'+GIT_DEPLOY_BRANCH)
    for temp_name in result:
        if temp_name.deleted_file:
            FILE_LISTING["A"].append(temp_name.b_path)
        elif temp_name.new_file:
            FILE_LISTING["D"].append(temp_name.b_path)
        elif temp_name.renamed_file:
            FILE_LISTING["A"].append(temp_name.rename_from)
            FILE_LISTING["D"].append(temp_name.rename_to)
        else:
            FILE_LISTING["M"].append(temp_name.b_path)
    return FILE_LISTING

def get_ignore_list(ftpignore_path):
    file_list = []
    file = open('.ftpignore','r+')
    for line in file:
        line = line.replace('\n','').replace('\t','')
        line =  os.path.join(SOURCE_DIR,line)
        file_list.append(line)
    return file_list



def ftp_transfer(source):
    pathlist = source.split(os.sep)
    ftpHandler.cwd(FTP_SOURCE_DIR)
    for name in pathlist:    
        if os.path.isfile(name):
            print("transfering file ",name)
            ftpHandler.storbinary("STOR "+name,open(name,'rb'))
        elif os.path.isdir(name):
            print("creating directory ",name)
            try:
                ftpHandler.mkd(name)
            except error_perm as err:
                #Ignore dir exists
                if not err.args[0].startswith('550'):
                    raise
            print("Switch directory to ",name)
            ftpHandler.cwd(name)
            os.chdir(name)
    for name in pathlist:        
        #return to root destination
        ftpHandler.cwd("..")
        os.chdir("..")

def ftp_transfer_file(path):
    for filename in os.listdir(path):
        ignore_files = get_ignore_list(IGNORE_FILE)
        localfile = os.path.join(path,filename)
        if localfile in ignore_files:
            print(localfile + " ignored")
        elif os.path.isfile(localfile):
            print("Transfering file ",localfile)
            ftpHandler.storbinary("STOR " + filename,open(localfile,'rb') )
        elif os.path.isdir(localfile):
            print("Making dir ",filename)
            try:
                ftpHandler.mkd(filename)
            except error_perm as err:
                #Ignore dir exists
                if not err.args[0].startswith('550'):
                    raise
            print("Switch directory to ",localfile)
            ftpHandler.cwd(filename)
            ftp_transfer_file(localfile)
            ftpHandler.cwd("..")

git_list = git_file_list()

ignore_list = get_ignore_list()
git_find_list = git_list["A"] + git_list["M"] + git_list["D"]

for filename in ignore_list:
    try:
        index = git_find_list.index(filename)
        git_find_list.remove(git_list[index])
    except ValueError:
       print("file not found in ignore ",filename)

for filename in git_find_list:
    
#ftp_transfer("testdir1/dir2/dir3/file3")
#before_transfer()
#ftp_transfer_file(SOURCE_DIR)
#ftpHandler.quit()
#print("ALL DONE")