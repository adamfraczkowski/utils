#Author AdamFraczkowski
import subprocess
from ftplib import FTP, error_perm
import os

ftpHandler = FTP()

# OPTIONS TO CHANGE
GIT_PATH = '/usr/bin/git'
GIT_DEPLOY_BRANCH = 'master'
IGNORE_FILE = '.ftpignore'
SOURCE_DIR = 'testdir1'
FTP_SERVER = 'ftp.dlptest.com'
FTP_PORT = 21
FTP_USERNAME = 'dlpuser@dlptest.com'
FTP_PASSWORD = 'VADPRDqid4TaB0r5a2B0n9wLp'
# ------------------
ftpHandler.connect(FTP_SERVER,FTP_PORT)
ftpHandler.login(FTP_USERNAME,FTP_PASSWORD)

def before_transfer():
    subprocess.call([GIT_PATH,'checkout',GIT_DEPLOY_BRANCH],cwd=SOURCE_DIR)
    #Add things to do before deploy

def get_ignore_list(ftpignore_path):
    file_list = []
    file = open('.ftpignore','r+')
    for line in file:
        line = line.replace('\n','').replace('\t','')
        line =  os.path.join(SOURCE_DIR,line)
        file_list.append(line)
    return file_list

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


before_transfer()
ftp_transfer_file(SOURCE_DIR)
ftpHandler.quit()
print("ALL DONE")