FROM ubuntu:latest
RUN apt-get -y update && apt-get install -y python-is-python3 git python3-venv sshpass nmap libmagic-dev ffmpeg

ENV USER=asparagus

RUN mkdir -p /home/asparagus/bin/hackerspace-scripts-2
RUN cp -R /etc/skel/. /home/asparagus
RUN chmod -R 777 /home/asparagus/.

RUN useradd -u 8877 asparagus
USER asparagus

COPY . /home/asparagus/bin/hackerspace-scripts-2

WORKDIR /home/asparagus/bin/hackerspace-scripts-2

CMD ["bash", "./control-panel"]