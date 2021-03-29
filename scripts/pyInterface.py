import sys
import logging
import json
import time
import census2xlsx

report_area = json.loads(sys.argv[1])
selected_indicators = json.loads(sys.argv[2])

logging.basicConfig(filemode="w", level=logging.INFO)
logger = logging.getLogger("pyInterface")

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", "%H:%M:%S"
)
fh = logging.FileHandler("pyInterface.log", "w+")
fh.setFormatter(formatter)

logger.addHandler(fh)

logger.info("Report Area: %s", report_area)
logger.info("Selected Indicators: %s", selected_indicators)

data_dir = "./src/assets/data"
log_dir = "./logs"
c2x = census2xlsx.Census2Xlsx(data_dir, log_dir)
options = {"outputPath": "./output/test.xlsx"}
c2x.generate_tables(report_area, selected_indicators, options)