`deployftp_sync.py`Script sync changes between commit and remote repository on ftp server

## Prerequests

* Python 3
* package `ftplib` installation `pip3 install ftplib`

## Config

Config using static variables at the beginning of script:

-----------------------------------------------------------------------------------------------------
| Name              | Description                                                                   |
|-------------------|-------------------------------------------------------------------------------|
| GIT_PATH          | Git system path (check command `whereis git`, default `/usr/bin/git` or `git`)|
| GIT_DEPLOY_BRANCH | Deploy branch                                                                 |                                     |
| GIT_REMOTE_NAME   | Remote name - default 'origin'
| SOURCE_DIR        | Source main project directory                                                 |
| FTP_SERVER        | FTP server address                                                            |
| FTP_PORT          | Port (default 21)                                                             |
| FTP_USERNAME      | FTP server username                                                           |
| FTP_PASSWORD      | FTP server password                                                           |
-----------------------------------------------------------------------------------------------------

## GIT integration

* Put `deploy_ftp.py` script in project root directory
* Determine python3 path (`whereis python3`, default `/usr/bin/python3` or `python3`)
* If you want to deploy project right before push to GIT, modify git `pre-push` hook.
* Inside your project create file `.git/hooks/pre-push` and write inside (for python3 path `/usr/bin/python3` and `/home/example-project-root-dir/` root project path):
```
/usr/bin/python3 /home/example-project-root-dir/deploy_ftp.py
```
* Make file `pre-push` executable `chmod u+x pre-push`
* If you want you can run script `./pre-push`. Python script should run and deploy files into FTP

Now, if you push  changes, the `deploy_ftp.py` script run and do the job
If you want , you can edit before transfer function to make some project builds etc before send files to ftp

