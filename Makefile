cqa:
	poetry run topyn .
	poetry run pytest -rf tests

	echo
	echo "OK 👍"

topyn-fix:
	poetry run topyn . --fix

run-dev-server:
	uvicorn main:app --reload

deploy:
	deta deploy
	