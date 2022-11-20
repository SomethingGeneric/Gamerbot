docker:
	./build_docker.sh
test: docker
	docker run gamerbot