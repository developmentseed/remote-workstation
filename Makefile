.PHONEY: install install-dev lint format diff deploy destroy ssh_config

install:
	npm install
	pipenv install

install-dev:
	npm install
	pipenv install --dev

lint:
	pipenv run flake8 cdk/ utils/
	pipenv run isort --check-only --profile black cdk/ utils/
	pipenv run black --check --diff cdk/ utils/

format:
	pipenv run isort --profile black cdk/ utils/
	pipenv run black cdk/ utils/

diff:
	pipenv run npx cdk diff --app cdk/app.py || true

deploy:
	pipenv run npx cdk deploy --app cdk/app.py --require-approval never && pipenv run python3 utils/generate_ssh_config.py

destroy:
	pipenv run npx cdk destroy --app cdk/app.py --force

ssh-config:
	pipenv run python3 utils/generate_ssh_config.py

ssh-to-instance:
	source .env && ssh -F $${SSH_CONFIG_LOCATION:-./.ssh/config} remote-workstation-$${IDENTIFIER:-dev}
