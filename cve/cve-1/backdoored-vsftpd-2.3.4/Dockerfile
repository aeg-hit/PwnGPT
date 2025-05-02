FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -y
RUN apt-get install -y git

WORKDIR /root/

RUN git clone https://github.com/Anon-Exploiter/vulnerable-packages && \
	cd vulnerable-packages && \
	cd backdoored-vsftpd-2.3.4 && \
	mv * /root/ && \
	cd /root && \
	rm -rfv vulnerable-packages

RUN apt-get purge -y git && \
	apt-get -y autoclean && \
	apt-get -y autoremove && \
	apt-get -y clean

RUN mkdir /usr/share/empty/ && \
	mkdir /var/ftp/ && \
	useradd -d /var/ftp ftp

RUN chown root.root /var/ftp && \
	chmod og-w /var/ftp

RUN mv vsftpd /usr/local/sbin/vsftpd && \
	mv vsftpd.conf /etc/

RUN echo 'echo Started FTP Server@ `hostname -i 2>/dev/null`:21' > /root/run.sh && \
	echo "/usr/local/sbin/vsftpd" >> /root/run.sh

CMD ["/bin/bash", "-c", "/bin/bash run.sh"]