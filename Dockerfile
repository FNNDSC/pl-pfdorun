# Docker file for pfdorun ChRIS plugin app
#
# Build with
#
#   docker build -t <name> .
#
# For example if building a local version, you could do:
#
#   docker build -t local/pl-pfdorun .
#
# In the case of a proxy (located at say http://proxy.tch.harvard.edu:3128), do:
#
#   export PROXY=http://proxy.tch.harvard.edu:3128
#   docker build --build-arg http_proxy=${PROXY} --build-arg UID=$UID -t local/pl-pfdorun .
#
# To run an interactive shell inside this container, do:
#
#   docker run -ti --entrypoint /bin/bash local/pl-pfdorun
#
# To pass an env var HOST_IP to container, do:
#
#   docker run -ti -e HOST_IP=$(ip route | grep -v docker | awk '{if(NF==11) print $9}') --entrypoint /bin/bash local/pl-pfdorun
#

FROM fnndsc/ubuntu-python3:latest
LABEL MAINTAINER="dev@babymri.org"

ARG UID=1001
ENV UID=$UID DEBIAN_FRONTEND=noninteractive

WORKDIR /usr/local/src
COPY . .
RUN pip install --upgrade pip                                   && \
    pip install -r requirements.txt                             && \
    pip install .                                               && \
    apt install -y zip unzip inetutils-tools                    && \
    apt install -y bc binutils  perl psmisc                     && \
    apt install -y tar uuid-dev                                 && \
    apt install -y neovim                                       && \
    apt install -y imagemagick                                  && \
    apt install -y tzdata                                       && \
    apt-get install -y locales                                  && \
    export LANGUAGE=en_US.UTF-8                                 && \
    export LANG=en_US.UTF-8                                     && \
    export LC_ALL=en_US.UTF-8                                   && \
    locale-gen en_US.UTF-8                                      && \
    dpkg-reconfigure locales                                    && \
    useradd -u $UID -ms /bin/bash localuser

# the precedent is for a plugin to be run like
# docker run --entrypoint /usr/bin/python fnndsc/pl-appname appname /in /out
# executable scripts are expected to be found in the working directory
WORKDIR /usr/local/bin
CMD ["pfdorun", "--help"]

