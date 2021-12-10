FROM opensciencegrid/software-base:fresh

RUN yum -y install vim && \
    yum -y install osg-xrootd-standalone && \
    yum -y install nvme-cli && \
    yum -y install xfsprogs

ADD osg-ca-generator-1.5.0 /osg-ca-generator-1.5.0

RUN cd osg-ca-generator-1.5.0 && \
    make install

ADD image-config.d/* /etc/osg/image-config.d/
