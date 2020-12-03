PYTHON = python3
SRC = src
LOGS = src/logs

.PHONY = help setup proto run debug test clean
.DEFAULT_GOAL = help

help:
	@echo "---------------HELP-----------------"
	@echo "To setup the project type make setup"
	@echo "To run the project prototype type make proto"
	@echo "To run the project type make run"
	@echo "To debug the project type make debug"
	@echo "To test the project type make test"
	@echo "To clean the project type make clean"
	@echo "------------------------------------"

setup:
	${PYTHON} tools.py

run:
	${PYTHON} ${SRC}/view.py

debug:
	${PYTHON} debug

test:
	${PYTHON} -m pytest
	
clean:
	rm ${LOGS}/*.log
