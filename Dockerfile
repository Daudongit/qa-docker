FROM centos:7

LABEL Vendor="CentOS" \
      License=GPLv2 \
      Version=2.4.6-40

RUN yum -y update


# install necessary tools
RUN yum install unzip -y
RUN yum -y install  https://centos7.iuscommunity.org/ius-release.rpm 
RUN yum -y update
RUN yum -y install python36u \
                   python36u-pip \
                   python36u-devel 


# install headless chrome
RUN curl -O  https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
RUN yum install google-chrome-stable_current_x86_64.rpm -y

# install selenium
RUN /bin/pip3.6 install selenium
# RUN /bin/pip3.6 install psutil==5.6.3
RUN /bin/pip3.6 install yagmail
RUN /bin/pip3.6 install configparser
RUN /bin/pip3.6 install pytest
RUN /bin/pip3.6 install pytest-xdist
RUN /bin/pip3.6 install pytest-html
RUN /bin/pip3.6 install beautifulsoup4
RUN /bin/pip3.6 install lxml

# download chromedriver
RUN mkdir /opt/chrome
RUN curl -O https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip -d /opt/chrome

# copy the testing python script
# COPY test/qa/ .

# File and Folder
COPY startup.sh /startup.sh
RUN chmod +x /startup.sh

COPY test/sample.py .
CMD ["/startup.sh"]