import React from "react";
import PropTypes from "prop-types";
import LocationPage from "./pages/LocationPage/LocationPage";
import IndicatorPage from "./pages/IndicatorPage/IndicatorPage";
import ConfirmationPage from "./pages/ConfirmationPage/ConfirmationPage";
import LoadingPage from "./pages/LoadingPage/LoadingPage";
import GraphPage from "./pages/GraphPage/GraphPage";
import "./css/AppSection.css";

const electron = window.require("electron");
const { ipcRenderer } = electron;

class AppSection extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      locationList: [],
      indicatorList: [],
      fileName: "",
      filePath: ipcRenderer.send("GET_DOWNLOADS_PATH"),
      progress: 0,
      progressDialog: "Starting your download",
    };

    this.setFileName = this.setFileName.bind(this);
    this.reset = this.reset.bind(this);
    this.confirmDownload = this.confirmDownload.bind(this);
    this.addLocation = this.addLocation.bind(this);
    this.removeLocation = this.removeLocation.bind(this);
    this.addIndicator = this.addIndicator.bind(this);
    this.removeIndicator = this.removeIndicator.bind(this);
    this.startPythonScript = this.startPythonScript.bind(this);

    const { onPageChange } = this.props;
    ipcRenderer.on("MESSAGE_FROM_BACKGROUND_VIA_MAIN", (event, args) => {
      console.log(args);
      const tmpMessage = args.split(" ");
      const newProgress = parseFloat(tmpMessage[tmpMessage.length - 1]) * 100;
      const newDialog = tmpMessage.slice(0, tmpMessage.length - 1).join(" ");

      this.setState({ progress: newProgress, progressDialog: newDialog });
      if (newProgress > 100) {
        onPageChange(1);
      }
    });

    ipcRenderer.on("RETURN_DIALOG", (event, args) => {
      if (args.filePath && args.filePath.length > 0) {
        this.setState({ filePath: args.filePath });
      }
    });

    ipcRenderer.on("RETURN_DOWNLOADS_PATH", (event, args) => {
      this.setState({ filePath: args.downloadsPath });
    });
  }

  setFileName(name) {
    const { setInvalidFileName } = this.props;
    this.setState({ fileName: name });
    setInvalidFileName(false);
  }

  reset() {
    const {
      setInvalidLocations,
      setInvalidIndicators,
      setInvalidFileName,
      setInvalidFilePath
    } = this.props;

    setInvalidLocations(true);
    setInvalidIndicators(true);
    setInvalidFileName(false);
    setInvalidFilePath(false);

    this.setState({
      locationList: [],
      indicatorList: [],
      fileName: "",
      filePath: ipcRenderer.send("GET_DOWNLOADS_PATH"),
      progress: 0,
      progressDialog: "Starting your download",
    });
  }

  confirmDownload() {
    const {
      setInvalidFileName,
      setInvalidFilePath
    } = this.props;

    const {
      fileName,
      filePath,
    } = this.state;

    if (fileName.length === 0) {
      setInvalidFileName(true);
      return false;
    }
    if (fileName.length === 0) {
      setInvalidFilePath(true);
      return false;
    }

    return true;
  }

  addLocation(locationName, geographicLevel, primaryID, secondaryID) {
    const { setInvalidLocations } = this.props;
    const { locationList } = this.state;
    const idx = locationList.findIndex(
      (i) => (
        i.geographicLevel === geographicLevel
        && i.primaryID === primaryID
        && i.secondaryID === secondaryID
      ),
    );
    if (idx === -1) {
      locationList.push({
        locationName,
        geographicLevel,
        primaryID,
        secondaryID,
      });
      this.setState({ locationList });
    }
    setInvalidLocations(false);
  }

  removeLocation(locationIdx) {
    const { setInvalidLocations } = this.props;
    const { locationList } = this.state;

    if (locationList.length > locationIdx) {
      locationList.splice(locationIdx, 1);
      this.setState({ locationList });
    }

    if (locationList.length === 0) {
      setInvalidLocations(true);
    }
  }

  addIndicator(sectionIdx, tableIdx, tableName) {
    const { setInvalidIndicators } = this.props;
    const { indicatorList } = this.state;

    const idx = indicatorList.findIndex(
      (i) => i.sectionIdx === sectionIdx && i.tableIdx === tableIdx,
    );

    if (idx === -1) {
      indicatorList.push({ tableName, sectionIdx, tableIdx });
      this.setState({ indicatorList });
    } else {
      console.log("tried to add an indicator twice");
    }

    console.log("Ind valid");
    setInvalidIndicators(false);
  }

  removeIndicator(sectionIdx, tableIdx) {
    const { setInvalidIndicators } = this.props;
    const { indicatorList } = this.state;

    const idx = indicatorList.findIndex(
      (i) => i.sectionIdx === sectionIdx && i.tableIdx === tableIdx,
    );

    if (idx !== -1) {
      indicatorList.splice(idx, 1);
      this.setState({ indicatorList });
    }

    console.log(indicatorList);

    if (indicatorList.length === 0) {
      console.log("Ind invalid");
      setInvalidIndicators(true);
    }
  }

  startPythonScript() {
    const {
      locationList,
      indicatorList,
      fileName,
      filePath,
    } = this.state;

    ipcRenderer.send("START_BACKGROUND_VIA_MAIN", {
      reportArea: locationList,
      selectedIndicators: indicatorList,
      options: { outputFile: `${filePath}\\${fileName}.xlsx` },
    });

    // ipcRenderer.send("FAKE_BACKGROUND_VIA_MAIN");
  }

  render() {
    const {
      page,
      invalidFileName,
      invalidFilePath,
    } = this.props;

    const {
      locationList,
      indicatorList,
      fileName,
      filePath,
      progress,
      progressDialog,
    } = this.state;

    let section;
    if (page === 0) {
      section = (
        <LocationPage
          locationList={locationList}
          onAddLocation={this.addLocation}
          onRemoveLocation={this.removeLocation}
        />
      );
    } else if (page === 1) {
      section = (
        <IndicatorPage
          indicatorList={indicatorList}
          onAddIndicator={this.addIndicator}
          onRemoveIndicator={this.removeIndicator}
        />
      );
    } else if (page === 2) {
      section = (
        <ConfirmationPage
          locationList={locationList}
          indicatorList={indicatorList}
          fileName={fileName}
          filePath={filePath}
          invalidFileName={invalidFileName}
          invalidFilePath={invalidFilePath}
          onFileNameChange={this.setFileName}
        />
      );
    } else if (page === 3) {
      section = (
        <LoadingPage
          progress={progress}
          progressDialog={progressDialog}
          onPageMount={this.startPythonScript}
        />
      );
    } else if (page === 4) {
      section = <GraphPage />;
    }
    return <div id="AppSection">{section}</div>;
  }
}

AppSection.propTypes = {
  page: PropTypes.number,
  onPageChange: PropTypes.func,
  setInvalidLocations: PropTypes.func,
  setInvalidIndicators: PropTypes.func,
  invalidFileName: PropTypes.bool,
  setInvalidFileName: PropTypes.bool,
  invalidFilePath: PropTypes.bool,
  setInvalidFilePath: PropTypes.func,
};
AppSection.defaultProps = {
  page: 0,
  onPageChange: null,
  setInvalidLocations: null,
  setInvalidIndicators: null,
  invalidFileName: false,
  setInvalidFileName: null,
  invalidFilePath: false,
  setInvalidFilePath: null,
};

export default AppSection;
