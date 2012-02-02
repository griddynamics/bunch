export PYTHONPATH:= ${PWD}
export BUNCH_DEPENDENCIES:=dependencies.txt

all:	help

help:
	@echo "make check"
	@echo "make unit"
	@echo "make check_dependencies"
	@echo "make clean"

check:	clean check_dependencies unit

check_dependencies:
	@echo "Checking for dependencies to run tests ..."
	@for dependency in `cat $$BUNCH_DEPENDENCIES`; do \
		python -c "import $$dependency" 2>/dev/null || (echo "You must install $$dependency in order to run bunch's tests" && exit 3) ; \
		done

unit: clean
	@echo "Running unit tests ..."
	@nosetests -s --verbosity=2 --with-coverage --cover-erase --cover-inclusive tests/unit --cover-package=bunch

clean:
	@printf "Cleaning up files that are already in .gitignore... "
	@for pattern in `cat .gitignore | grep -v idea`; do find . -path "$$pattern" -delete; done
	@echo "OK!"
