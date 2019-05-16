#!bin/bash
apt-get update
apt-get install -y curl
apt-get install -y git
curl -O -J -L  https://dl.google.com/go/go1.11.4.linux-amd64.tar.gz
tar -C /usr/local -xzf go1.11.4.linux-amd64.tar.gz
mkdir /home/$USER/go
add-apt-repository ppa:phoerious/keepassxc
apt-get update
apt-get install -y keepassxc
curl -O -J -L  https://release.gitkraken.com/linux/gitkraken-amd64.deb
dpkg -i gitkraken-amd64.deb
apt-get install -f
dpkg -i gitkraken-amd64.deb
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 931FF8E79F0876134EDDBDCCA87FF9DF48BF1C90
echo deb http://repository.spotify.com stable non-free | sudo tee /etc/apt/sources.list.d/spotify.list
apt-get update
apt-get install -y spotify-client
apt-get install -y vlc
sudo echo "deb http://cz.archive.ubuntu.com/ubuntu xenial main universe" >> /etc/apt/sources.list
apt-get update
apt-get install -y brasero
curl -O -J -L  https://github.com/balena-io/etcher/releases/download/v1.4.9/balena-etcher-electron-1.4.9-linux-ia32.zip
apt-get install -y unzip
mkdir etcher
unzip balena-etcher-electron-1.4.9-linux-ia32.zip -d /home/$USER/etcher
curl -O -J -L  https://download.teamviewer.com/download/linux/teamviewer_amd64.deb
dpkg -i teamviewer_amd64.deb
apt-get install -f
dpkg -i teamviewer_amd64.deb
add-apt-repository ppa:krzemin/qnapi
apt-get update
apt-get install -y qnapi
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo install -o root -g root -m 644 microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main" > /etc/apt/sources.list.d/vscode.list'
apt-get install -y apt-transport-https
apt-get update
apt-get install -y code
apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io
groupadd docker
usermod -aG docker $USER
chown -R $USER:$USER .
chown -R $USER:$USER /home/$USER/go
apt-get install -y build-essential

curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -
apt-get update
apt-get install -y nodejs
apt install -y libgnome-keyring0
curl -O -J -L https://www.dropbox.com/download?dl=packages/ubuntu/dropbox_2018.11.28_amd64.deb
dpkg -i dropbox_2018.11.28_amd64.deb
apt-get install -f
dpkg -i dropbox_2018.11.28_amd64.deb
curl -O -J -L https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb
apt-get install -f
dpkg -i google-chrome-stable_current_amd64.deb
apt-get install -y python3-pip
apt-get install -y sqlite3
add-apt-repository -y ppa:linuxgndu/sqlitebrowser
apt-get update
apt-get install -y sqlitebrowser
curl -L "https://github.com/docker/compose/releases/download/1.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get -y install oracle-java8-installer
sudo apt-get -y install oracle-java8-set-default
curl -O -J -L https://dl.google.com/dl/android/studio/ide-zips/3.4.0.18/android-studio-ide-183.5452501-linux.tar.gz
tar -xf android-studio-ide-183.5452501-linux.tar.gz -C /opt/
chown -R $USER:$USER /opt/android-studio
apt-get install -y libc6:i386 libncurses5:i386 libstdc++6:i386 lib32z1 libbz2-1.0:i386
apt-get install -y npm
npm install vue
npm install -g @vue/cli
add-apt-repository multiverse && sudo apt-get update
apt-get install -y virtualbox
apt-get install gparted
