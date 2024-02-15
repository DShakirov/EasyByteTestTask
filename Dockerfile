FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set app directory
ARG APP_DIR=/usr/src/app

# Set work directory
WORKDIR ${APP_DIR}

RUN apt-get update \
    # Installing dependencies
    && apt install -yq libpq-dev gettext build-essential \
            libgl1 libbz2-dev zlib1g-dev supervisor gnupg \
            libncurses5-dev libgdbm-dev libnss3-dev curl \
            libssl-dev libreadline-dev libffi-dev wget  libglib2.0-0 \
    # cleaning up unused files
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

#Set dependence
COPY requirements.txt ./

# Install dependencies
RUN pip3 install --default-timeout=200 -r ./requirements.txt

#Create and copy project
COPY . .

## Virtual environment activation
ENV PATH="${APP_DIR}/venv/bin:$PATH"

ENTRYPOINT [ "python3", "dispatcher.py" ]