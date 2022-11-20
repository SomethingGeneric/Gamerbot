mkdocker:
	./build_docker.sh
test: mkdocker
	docker run gamerbot
run: mkdocker
	docker run -d gamerbot