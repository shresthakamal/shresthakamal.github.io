push:
	git add .
	git commit -m "update"
	git push origin master

build:
	@echo "Building..."
	bundle exec jekyll build

serve:
	@echo "Serving..."
	bundle exec jekyll serve --lsi

start:
	make build
	make serve