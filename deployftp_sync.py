#Author AdamFraczkowski
import subprocess
from git import Repo
from ftplib import FTP, error_perm
import os

ftpHandler = FTP()

# OPTIONS TO CHANGE
GIT_DEPLOY_BRANCH = 'master'
GIT_REMOTE_NAME = 'origin'
SOURCE_DIR = '.'

FTP_SOURCE_DIR = 'deploy'
FTP_MAIN_DIR ='/home/adam/ftpserver'

GIT_PATH= '/usr/bin/git'

FTP_SERVER = '127.0.0.1'
FTP_PORT = 21
FTP_USERNAME = 'adam'
FTP_PASSWORD = ''
# ------------------
gitrepo = Repo(SOURCE_DIR)

ftpHandler.connect(FTP_SERVER,FTP_PORT)
ftpHandler.login(FTP_USERNAME,FTP_PASSWORD)

def before_transfer():
    print("before transfer task...")
    #subprocess.call([GIT_PATH,'checkout',GIT_DEPLOY_BRANCH],cwd=SOURCE_DIR)

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
    ftpHandler.cwd(FTP_MAIN_DIR)
    os.chdir(SOURCE_DIR)

def delete_ftp(source):
    try:
        ftpHandler.cwd(FTP_MAIN_DIR)
        ftpHandler.cwd(source)
    except:
        print("NO FILE ON FTP SERVER ",source)

git_list = git_file_list()
git_find_list = git_list["A"] + git_list["M"]

print("files to transfer")
print(git_find_list)
print("files to delete")
print(git_list["D"])
before_transfer()    
for path in git_find_list:
    ftp_transfer(path)
ftpHandler.quit()
print("ALL DONE")