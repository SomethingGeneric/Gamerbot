docker:
	./build_docker.
test: docker
	docker run gamerbot