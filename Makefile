.PHONY: deploy
deploy:
	chalice deploy --profile sandbox

.PHONY: test
test:
	http https://traceback-redirect.wordstream-sandbox.com/api/traceback/1337
