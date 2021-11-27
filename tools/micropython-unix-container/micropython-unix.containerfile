FROM ubuntu:20.04

# This fixes stupid tzdata package: https://dev.to/setevoy/docker-configure-tzdata-and-timezone-during-build-20bk
ENV TZ=America/Los_Angeles
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Install dependencies
RUN apt-get update && \
    apt-get install -y build-essential libffi-dev git pkg-config python python3

##### Checkout #####
# alternatively could mount a volume /usr/src/micropython instead
RUN git clone https://github.com/micropython/micropython.git /usr/src/micropython

# Go to the source working dir
#WORKDIR /usr/src/micropython
WORKDIR /usr/src/micropython/ports/unix

# from https://github.com/micropython/micropython/#the-unix-version
RUN make submodules && \
    make

RUN make test

# essentially copies microptyhon binary to /usr/local/bin/micropython
RUN make install

#CMD ["/usr/local/bin/micropython"]
CMD ["/bin/bash"]
