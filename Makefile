.PHONY: deploy
deploy: dev-dependencies
	chalice deploy --profile sandbox

.PHONY: dev-dependencies
dev-dependencies:
	pip install -r requirements.txt

.PHONY: test
test:
	http https://traceback-redirect.wordstream-sandbox.com/api/traceback/927461670283046927
	http https://traceback-redirect.wordstream-sandbox.com/api/traceback/911984663319474183
