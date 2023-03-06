FROM opensciencegrid/software-base:fresh

RUN yum -y install vim && \
    yum -y install osg-xrootd-standalone && \
    yum -y install osg-ca-certs && \
    yum -y install iproute 

ADD 5fca1cb1.0 /etc/grid-security/certificates/5fca1cb1.0
ADD 5fca1cb1.signing_policy /etc/grid-security/certificates/5fca1cb1.signing_policy 
ADD grid-mapfile /etc/grid-security/grid-mapfile
ADD checksum/* /etc/xrootd/checksum/

ADD auth-file /etc/xrootd/auth-file
COPY setup.sh /setup.sh

ADD image-config.d/* /etc/osg/image-config.d/
