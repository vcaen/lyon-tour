apt-get update && apt-get install -y \
	build-essential \
	python-dev \
	python-pip \
	curl \
	libmysqlclient-dev \
	python-mysqldb

pip install -r /app/env/server/requirements.txt

