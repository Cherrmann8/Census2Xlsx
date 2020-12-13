PYTHON = python3
SRC = src
DATA = src/data
LOG = logs
OUT = output

.PHONY = help setup clean model model_debug view view_debug test
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
	${PYTHON} ${SRC}/tools.py -d ${DATA}

clean:
	rm -rf ${LOG}/* ${OUT}/* ${SRC}/__pycache__

model:
	${PYTHON} ${SRC}/model.py -d ${DATA} -o ${OUT}

model_debug:
	${PYTHON} ${SRC}/model.py -d ${DATA} -o ${OUT} -l ${LOG}

view:
	${PYTHON} -d ${SRC}/view.py -d ${DATA} -o ${OUT}

view_debug:
	${PYTHON} ${SRC}/view.py -d ${DATA} -o ${OUT} -l ${LOG}

test:
	${PYTHON} -m pytest

