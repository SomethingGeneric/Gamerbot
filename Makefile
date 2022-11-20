mkdocker:
	./build_docker.sh
test: mkdocker
	./run_docker.sh
run: mkdocker
	./run_docker.sh -d