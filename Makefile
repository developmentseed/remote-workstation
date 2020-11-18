.PHONEY: lint format diff deploy destroy ssh_config

lint:
	PIPENV_DOTENV_LOCATION=.env pipenv run flake8 .
	PIPENV_DOTENV_LOCATION=.env pipenv run isort --check-only --profile black .
	PIPENV_DOTENV_LOCATION=.env pipenv run black --check --diff .

format:
	PIPENV_DOTENV_LOCATION=.env pipenv run isort --profile black .
	PIPENV_DOTENV_LOCATION=.env pipenv run black .

diff:
	PIPENV_DOTENV_LOCATION=.env pipenv run cdk diff || true

deploy:
	PIPENV_DOTENV_LOCATION=.env pipenv run cdk deploy --require-approval never && pipenv run python3 utils/generate_ssh_config.py

destroy:
	PIPENV_DOTENV_LOCATION=.env pipenv run cdk destroy --force

ssh_config:
	PIPENV_DOTENV_LOCATION=.env pipenv run python3 utils/generate_ssh_config.py
