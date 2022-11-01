setup:
	pip install pipenv
	pipenv install --dev
	pipenv shell
init:
	pipenv install --dev
	pipenv shell
pre_commit_install:
	pre-commit install

quality_check:
	isort --profile=black .
	black .
	pylint --recursive=y .

build:
	sudo bash boot/docker/compose/trip_duration_prediction/my_build.sh build

down:
	sudo bash boot/docker/compose/trip_duration_prediction/my_build.sh down

up:
	sudo bash boot/docker/compose/trip_duration_prediction/my_build.sh up

test:
	pytest tests/
