FROM debian:bullseye

RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    lsb-release \
    software-properties-common \
    sudo

RUN echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list && \
    wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - && \
    apt-get update && \
    apt-get install -y postgresql postgresql-contrib

EXPOSE 5432

CMD ["/usr/lib/postgresql/13/bin/postgres", "-D", "/var/lib/postgresql/data"]