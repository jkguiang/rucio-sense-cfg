FROM opensciencegrid/software-base:fresh

RUN yum -y install vim && \
    yum -y install osg-xrootd-standalone

ADD osg-ca-generator-1.5.0 /osg-ca-generator-1.5.0

RUN cd osg-ca-generator-1.5.0 && \
    make install

ADD 5fca1cb1.0 /etc/grid-security/certificates/5fca1cb1.0
ADD 5fca1cb1.signing_policy /etc/grid-security/certificates/5fca1cb1.signing_policy 
ADD grid-mapfile /etc/grid-security/grid-mapfile

ADD auth-file /etc/xrootd/auth-file

ADD image-config.d/* /etc/osg/image-config.d/
