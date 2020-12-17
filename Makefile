PYTHON = python3
SRC = src
DATA = assets/data
LOG = logs
OUT = output

.PHONY = help setup clean model_debug model view_debug view test build_debug
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
	rm -f ${LOG}/* ${OUT}/*

model_debug:
	${PYTHON} ${SRC}/model.py -d ${DATA} -o ${OUT} -l ${LOG}

model:
	${PYTHON} ${SRC}/model.py -d ${DATA} -o ${OUT}

view_debug:
	${PYTHON} ${SRC}/view.py -d ${DATA} -o ${OUT} -l ${LOG}

view:
	${PYTHON} ${SRC}/view.py -d ${DATA} -o ${OUT}

test:
	${PYTHON} -m pytest

build:
	pyinstaller --noconsole --onefile ${SRC}/view.py
