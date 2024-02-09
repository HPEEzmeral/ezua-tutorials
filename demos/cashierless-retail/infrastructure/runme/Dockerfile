###### 
# Future Releases should include
# Password Change of Jupyter Hub
#
#####
FROM rockylinux:8.6

ENV NB_USER dderichswei
ENV NB_UID 1000
ENV HOME /home/${NB_USER}

ENV ANSIBLE_LIBRARY=${HOME}/.hponeview/oneview-ansible/library
ENV ANSIBLE_MODULE_UTILS=${HOME}/.hponeview/oneview-ansible/library/module_utils



ENV NB_PASSWORD hpecp
ENV GOPATH /home/${NB_USER}/go
ENV GOROOT /usr/local/bin/go


ARG MAPR_VERSION_CORE="7.0.0"
ARG MAPR_VERSION_MEP="8.1.0"
ARG MAPR_REPO_ROOT="https://package.mapr.com/releases"
 
LABEL mapr.os=centos7 mapr.version=$MAPR_VERSION_CORE mapr.mep_version=$MAPR_VERSION_MEP
 
# ENV container docker
# RUN echo $(head -1 /etc/hosts | cut -f1) $HOST_NAME >> /etc/hosts

RUN echo "root:hpecp" | chpasswd && \
    yum -y groupinstall "Development Tools" && \
    yum -y install autoconf automake libtool jq && \  
    yum -y install epel-release && yum repolist  && \
    yum update -y  && \
    yum install -y yum-utils curl initscripts net-tools sudo wget which syslinux openssl file java-1.8.0-openjdk-devel unzip python39-pip.noarch python39-devel gcc git-all bzip2 glibc-locale-source sshpass
#  sshpass python3-crypto python3-psutil

# upgrade pip3
RUN pip3 install --no-cache-dir --upgrade pip

### Install Docker-CLI
RUN yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo  && \
    yum -y install docker-ce-cli 

## Install MAPR (does currently not work with PODMAN :-()
RUN mkdir -p /opt/mapr/installer/docker/ && \
    wget "${MAPR_REPO_ROOT}/installer/redhat/mapr-setup.sh" -P /opt/mapr/installer/docker/ && \
    chmod +x /opt/mapr/installer/docker/mapr-setup.sh

RUN /opt/mapr/installer/docker/mapr-setup.sh -r "$MAPR_REPO_ROOT" container client "$MAPR_VERSION_CORE" "$MAPR_VERSION_MEP" mapr-client mapr-hbase mapr-spark mapr-kafka mapr-livy


#### Install ZSH
RUN git clone https://github.com/powerline/fonts.git --depth=1 && \
    cd fonts && ./install.sh && \ 
    yum -y install zsh


#RUN yum install -y make ncurses-devel gcc autoconf man
#RUN git clone -b zsh-5.7.1 https://github.com/zsh-users/zsh.git /tmp/zsh
#RUN cd /tmp/zsh && ./Util/preconfig && ./configure && make -j 20 install.bin install.modules install.fns


#### Install Kubectl
RUN echo '[kubernetes]'  > /etc/yum.repos.d/kubernetes.repo && \
    echo 'name=Kubernetes'  >> /etc/yum.repos.d/kubernetes.repo && \
    echo 'baseurl=https://packages.cloud.google.com/yum/repos/kubernetes-el7-x86_64'  >> /etc/yum.repos.d/kubernetes.repo && \
    echo 'enabled=1'  >> /etc/yum.repos.d/kubernetes.repo && \
    echo 'gpgcheck=1'  >> /etc/yum.repos.d/kubernetes.repo && \
    echo 'repo_gpgcheck=1'  >> /etc/yum.repos.d/kubernetes.repo && \ 
    echo 'gpgkey=https://packages.cloud.google.com/yum/doc/yum-key.gpg https://packages.cloud.google.com/yum/doc/rpm-package-key.gpg'  >> /etc/yum.repos.d/kubernetes.repo && \
    yum install -y kubectl

#### Install kubectx
RUN git clone https://github.com/ahmetb/kubectx /opt/kubectx &&  ln -s /opt/kubectx/kubectx /usr/local/bin/kubectx && ln -s /opt/kubectx/kubens /usr/local/bin/kubens && \
    cd /opt/ && curl -k https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash && \
    pip3 --no-cache-dir install matplotlib numpy pandas wheel psutil  

#RUN rm /etc/yum.repos.d/mapr_*.repo && \
#    yum -q clean all && \
#    rm -rf /var/lib/yum/history/* && \
#    find /var/lib/yum/yumdb/ -name origin_url -exec rm {} \;

#### Powershell
RUN curl https://packages.microsoft.com/config/rhel/7/prod.repo | sudo tee /etc/yum.repos.d/microsoft.repo && \
    yum update -y && \
    yum install -y powershell

#### NODEJS
RUN curl -sL https://rpm.nodesource.com/setup_16.x | bash - && \
    yum -y install nodejs

# RUN yum -y install nodejs    # this does not work anymore

 
#### GO
RUN wget https://golang.org/dl/go1.19.linux-amd64.tar.gz && \
    tar -C /usr/local/bin -xf go1.19.linux-amd64.tar.gz && \
    rm go1.19.linux-amd64.tar.gz && \
    echo "export PATH=$PATH:/usr/local/bin/go/bin" >> /etc/profile
ENV PATH $PATH:/usr/local/bin/go/bin:/home/${NB_USER}/.local/bin/

##### K9S
RUN echo "Downloading k9s" && \
    rm -r k9s || true && \
    wget https://github.com/derailed/k9s/releases/download/v0.26.3/k9s_Linux_x86_64.tar.gz && \
    tar xvfz k9s_Linux_x86_64.tar.gz && \
    mv 'k9s' /usr/local/bin/ && \
    rm k9s_Linux_x86_64.tar.gz

###### Python3
RUN ls /usr/bin/python*


RUN ln -s /usr/bin/python3.9 /usr/bin/python && \
    rm /usr/bin/python3 && \
    ln -s /usr/bin/python3.9 /usr/bin/python3 && \
    ln -s /usr/bin/pip3 /usr/bin/pip

##### cleaning the environment
RUN rm -rf /var/cache/yum

### Install Powershell (part1)
RUN curl https://packages.microsoft.com/config/rhel/7/prod.repo | sudo tee /etc/yum.repos.d/microsoft.repo && \
    yum update -y && \
    yum install -y powershell         

### Install Operator SDK
ENV RELEASE_VERSION=v0.18.0
# Linux
RUN curl -LO https://github.com/operator-framework/operator-sdk/releases/download/${RELEASE_VERSION}/operator-sdk-${RELEASE_VERSION}-x86_64-linux-gnu && \
    mv operator-sdk-${RELEASE_VERSION}-x86_64-linux-gnu /usr/local/bin/operator-sdk && \
    chmod +x /usr/local/bin/operator-sdk

RUN useradd \
    -c "Default user" \
    -d /home/${NB_USER} \
    -u ${NB_UID} \
    ${NB_USER} && \
    chown -R ${NB_USER} ${HOME} && \
    usermod -aG docker ${NB_USER}


### Install R
#RUN dnf install epel-release && \
#    dnf config-manager --set-enabled powertools && \
#    yum install R -y

USER ${NB_USER}

###### HPONEVIEW Ansible Library
RUN mkdir ${HOME}/.hponeview
RUN git -C ${HOME}/.hponeview clone https://github.com/HewlettPackard/oneview-ansible.git
# RUN pip3 install --no-cache-dir --user -r requirements.txt

#### ZSH
RUN cd && \
    git clone https://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh && \
    cp ~/.oh-my-zsh/templates/zshrc.zsh-template ~/.zshrc && \
    sed -i 's/robbyrussell/agnoster/g' ~/.zshrc && \
    git clone --depth=1 https://github.com/romkatv/powerlevel10k.git /home/${NB_USER}/.oh-my-zsh/custom/themes/powerlevel10k && \
    sed -i 's/agnoster/powerlevel10k\/powerlevel10k/g' ~/.zshrc

### add GO jupyter_kernel

#RUN cd /home/${NB_USER} && \
#    chown dderichswei:dderichswei  . -R && \
#    export GO111MODULE=on && \
#    go get -d -u github.com/gopherdata/gophernotes && \
#    mkdir -p /home/${NB_USER}/.local/share/jupyter/kernels/gophernotes && \  
#    cd /home/${NB_USER}/.local/share/jupyter/kernels/gophernotes && \
#    cp /home/${NB_USER}/go/pkg/mod/github.com/gopherdata/gophernotes@v0.7.5/kernel/* /home/${NB_USER}/.local/share/jupyter/kernels/gophernotes && \
#    mkdir /home/${NB_USER}/go/bin && \
#    chmod +w /home/${NB_USER}/.local/share/jupyter/kernels/gophernotes/kernel.json && \
#    sed "s|gophernotes|$(go env GOPATH)/bin/gophernotes|" < kernel.json.in > kernel.json && \
#    echo /home/${NB_USER}

RUN pip --version
RUN python --version

# pip3 install --no-cache-dir --user kopf && \
RUN pip3 install --no-cache-dir --user matplotlib numpy pandas wheel psutil && \
    pip3 install --no-cache-dir --user ansible && \
    pip3 install --no-cache-dir --user hponeview && \
    pip3 install --no-cache-dir --user python-hpilo && \
    pip3 install --no-cache-dir --user pyvmomi && \
    pip3 install --no-cache-dir --user requests-ftp && \
    pip3 install --no-cache-dir --user wrapt && \
    pip3 install --no-cache-dir --user lxml && \
    pip3 install --no-cache-dir --user jupyterlab && \
    pip3 install --no-cache-dir --user notebook && \
    pip3 install --no-cache-dir --user jq && \
    pip3 install --no-cache-dir --user pandoc && \
    cd /home/${NB_USER} && \
    pip3 install --no-cache-dir --user bash_kernel && \
    python3  -m bash_kernel.install && \
    pip3 install --no-cache-dir --user jupyter_contrib_nbextensions && \
    /home/${NB_USER}/.local/bin/jupyter nbextensions_configurator enable --user && \
    /home/${NB_USER}/.local/bin/jupyter contrib nbextension install --user && \
    /home/${NB_USER}/.local/bin/jupyter nbextension enable toc2/main --user && \
    /home/${NB_USER}/.local/bin/jupyter nbextension enable execute_time/ExecuteTime --user


### Jupyter Notebook
CMD mkdir /home/${NB_USER}/notebooks && cd /home/${NB_USER}/notebooks &&\
   /home/${NB_USER}/.local/bin/jupyter-notebook --port 8889 --ip 0.0.0.0 --NotebookApp.password='' --NotebookApp.token='' & \
   cd /home/${NB_USER}/notebooks &&\
   /home/${NB_USER}/.local/bin/jupyter-lab --no-browser --ip 0.0.0.0 --port 8888 --NotebookApp.password='' --NotebookApp.token='' 


### change Usercontext to root
USER root


### Install Jupyter Kernel for R
#RUN R -e "install.packages('repr', repos='http://cran.rstudio.com/')" && \
#    R -e "install.packages('IRdisplay', repos='http://cran.rstudio.com/')" && \
#    R -e "install.packages('evaluate', repos='http://cran.rstudio.com/')" && \
#    R -e "install.packages('crayon', repos='http://cran.rstudio.com/')" && \
#    R -e "install.packages('pbdZMQ', repos='http://cran.rstudio.com/')" && \
#    R -e "install.packages('devtools', repos='http://cran.rstudio.com/')" && \
#    R -e "install.packages('uuid', repos='http://cran.rstudio.com/')" && \
#    R -e "install.packages('digest', repos='http://cran.rstudio.com/')" 
#    
#RUN R -e "install.packages('IRkernel', repos='http://cran.rstudio.com/')" && \
#    R -e "IRkernel::installspec()"


### GO Jupyter Kernel hack
#RUN env GO111MODULE=off go get -d -u github.com/gopherdata/gophernotes && \
#    cd "$(go env GOPATH)"/src/github.com/gopherdata/gophernotes && \
#    env GO111MODULE=on go install 
    # mv /root/go/bin/gophernotes /home/${NB_USER}/go/bin && \
    # chown ${NB_USER}:${NB_USER}} /home/${NB_USER}/go/bin/gophernotes


### HPECP Modul installation
RUN echo "${NB_USER}:hpecp" | chpasswd && \
    usermod -aG wheel ${NB_USER} && \
    mkdir -p /mnt/c/Users/${NB_USER}/.minikube/profiles/minikube/ && \
    chown ${NB_USER}:${NB_USER} /mnt/c/ -R

### DEP Installation
ENV GOBIN /usr/local/bin/go/bin 
RUN curl https://raw.githubusercontent.com/golang/dep/master/install.sh | sh 



### install latest ARGOCD CLI Installation
RUN VERSION=$(curl --silent "https://api.github.com/repos/argoproj/argo-cd/releases/latest" | grep '"tag_name"' | sed -E 's/.*"([^"]+)".*/\1/') && \
    curl -sSL -o /usr/local/bin/argocd https://github.com/argoproj/argo-cd/releases/download/$VERSION/argocd-linux-amd64 && \
    chmod +x /usr/local/bin/argocd

# get robotmonofonts
#RUN wget --content-disposition -P /usr/share/fonts/truetype/robotomono https://github.com/google/fonts/blob/master/apache/robotomono/static/RobotoMono-{Bold,BoldItalic,Italic,Light,LightItalic,Medium,MediumItalic,Regular,Thin,ThinItalic}.ttf?raw=true && \
#    fc-cache


# Install Hashicorp Vault
RUN yum install -y yum-utils && \
    yum-config-manager --add-repo https://rpm.releases.hashicorp.com/RHEL/hashicorp.repo && \
    yum -y install packer vault terraform && \
    setcap cap_ipc_lock= /usr/bin/vault

# dderichswei sudo without password
RUN echo "${NB_USER}   ALL=(ALL)    NOPASSWD: ALL" >> /etc/sudoers

## add PATH
RUN echo "export PATH=$PATH:/home/${NB_USER}/.krew/bin" >> /etc/profile


### govc Installation
#RUN curl -L https://github.com/vmware/govmomi/releases/download/v0.24.0/govc_linux_amd64.gz | gunzip > /usr/local/bin/govc && \
#    chmod +x /usr/local/bin/govc

### PDF Support
RUN dnf install epel-release
RUN yum install -y texlive

USER ${NB_USER}

### add powershell_kernel
RUN pip3 install --no-cache-dir --user powershell_kernel && \
    python3 -m powershell_kernel.install && \
    pip3 install pyVim --user --no-cache-dir 

RUN ssh-keygen -b 2048 -t rsa -f /home/${NB_USER}/.ssh/id_rsa -N ""

### add scrapy
RUN pip3 install --no-cache-dir --user scrapy

### add request
RUN pip3 install --no-cache-dir --user requests 

### add request
RUN pip3 install --no-cache-dir --user beautifulsoup4

## Jupyter Notebook export to PDF
RUN pip3 install --no-cache-dir --user pyppeteer

### Jupyter Lab Git Support
RUN pip3 install --no-cache-dir --user jupyterlab-git
RUN /home/${NB_USER}/.local/bin/jupyter lab build

### Add completion 
###
### Disabled     pip3 install --no-cache-dir --user jupyterlab-git && \
RUN pip3 install --no-cache-dir --user python-language-server && \
    pip3 install --no-cache-dir --user jupyter-tabnine && \
    /home/${NB_USER}/.local/bin/jupyter nbextension install --user --py jupyter_tabnine && \
    /home/${NB_USER}/.local/bin/jupyter nbextension enable --user --py jupyter_tabnine && \
    /home/${NB_USER}/.local/bin/jupyter serverextension enable --user --py jupyter_tabnine && \
    /home/${NB_USER}/.local/bin/jupyter labextension install @jupyter-widgets/jupyterlab-manager    && \
    /home/${NB_USER}/.local/bin/jupyter labextension install jupyter-leaflet   && \
    /home/${NB_USER}/.local/bin/jupyter lab build

### Krew Installation
RUN (  set -x; cd "$(mktemp -d)" && \
  OS="$(uname | tr '[:upper:]' '[:lower:]')" && \
  ARCH="$(uname -m | sed -e 's/x86_64/amd64/' -e 's/\(arm\)\(64\)\?.*/\1\2/' -e 's/aarch64$/arm64/')" && \
  curl -fsSLO "https://github.com/kubernetes-sigs/krew/releases/latest/download/krew-linux_amd64.tar.gz" && \
  tar zxvf krew-linux_amd64.tar.gz && \
  KREW=./krew-"${OS}_${ARCH}" && \
  "$KREW" install krew )


### neat Installation 
RUN PATH="${KREW_ROOT:-$HOME/.krew}/bin:$PATH" && \
    kubectl krew install neat && \
    echo "export PATH=$PATH:/home/${NB_USER}/.krew/bin" >> /home/${NB_USER}/.zshrc && \
    echo "export PATH=$PATH:/home/${NB_USER}/.krew/bin" >> /home/${NB_USER}/.bashrc 

### boto3 (s3 for python installation)
RUN pip3 install --no-cache-dir --user boto3


### define TERM environment
ENV TERM=linux
ENV TEST=TEST
  
EXPOSE 8888 80
EXPOSE 8889 81
