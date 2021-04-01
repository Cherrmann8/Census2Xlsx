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
      filePath: "",
      progress: 0,
      progressDialog: "",
      invalidStatus: {
        invalidLocations: false,
        invalidIndicators: false,
        invalidFileName: false,
        invalidFilePath: false,
      }
    };

    this.setFileName = this.setFileName.bind(this);
    this.addLocation = this.addLocation.bind(this);
    this.removeLocation = this.removeLocation.bind(this);
    this.addIndicator = this.addIndicator.bind(this);
    this.removeIndicator = this.removeIndicator.bind(this);
    this.startPythonScript = this.startPythonScript.bind(this);

    const { onPageChange } = this.props;
    ipcRenderer.on("MESSAGE_FROM_BACKGROUND_VIA_MAIN", (event, args) => {
      const tmpMessage = args.split(" ");
      const newProgress = parseFloat(tmpMessage[tmpMessage.length - 1]) * 100;
      const newDialog = tmpMessage.slice(0, tmpMessage.length - 1).join(" ");

      this.setState({ progress: newProgress, progressDialog: newDialog });
      if (newProgress >= 100) {
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

    ipcRenderer.send("GET_DOWNLOADS_PATH");
  }

  setFileName(name) {
    const { invalidStatus } = this.state;
    this.setState({ fileName: name });
    if (invalidStatus.invalidFileName) {
      this.setState({
        invalidStatus: {
          invalidLocations: invalidStatus.invalidLocations,
          invalidIndicators: invalidStatus.invalidIndicators,
          invalidFileName: false,
          invalidFilePath: invalidStatus.invalidFilePath,
        }
      });
    }
  }

  reset() {
    this.setState({
      locationList: [],
      indicatorList: [],
      fileName: "",
      progress: 0,
      progressDialog: "",
      invalidStatus: {
        invalidLocations: false,
        invalidIndicators: false,
        invalidFileName: false,
        invalidFilePath: false,
      }
    });
  }

  addLocation(locationName, geographicLevel, primaryID, secondaryID) {
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
  }

  removeLocation(locationIdx) {
    const { locationList } = this.state;

    if (locationList.length > locationIdx) {
      locationList.splice(locationIdx, 1);
      this.setState({ locationList });
    }

    console.log("appsection");
    console.log(locationList);
  }

  addIndicator(sectionIdx, tableIdx, tableName) {
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

    console.log(indicatorList);
  }

  removeIndicator(sectionIdx, tableIdx) {
    const { indicatorList } = this.state;
    const idx = indicatorList.findIndex(
      (i) => i.sectionIdx === sectionIdx && i.tableIdx === tableIdx,
    );
    if (idx !== -1) {
      indicatorList.splice(idx, 1);
      this.setState({ indicatorList });
    }

    console.log(indicatorList);
  }

  confirmDownload() {
    const {
      locationList,
      indicatorList,
      fileName,
      filePath,
      invalidStatus
    } = this.state;

    let invalidLoc = false;
    let invalidInd = false;
    let invalidName = false;
    let invalidPath = false;

    if (locationList.length === 0) {
      invalidLoc = true;
    }

    if (indicatorList.length === 0) {
      invalidInd = true;
    }

    if (fileName.length === 0) {
      invalidName = true;
    }

    this.setState({ invalidStatus: {
      invalidLocations: invalidLoc,
      invalidIndicators: invalidInd,
      invalidFileName: invalidName,
      invalidFilePath: invalidPath,
    } });

    if (invalidLoc || invalidInd || invalidName || invalidPath) {
      return false;
    }

    return true;
  }

  startPythonScript() {
    const { locationList, indicatorList } = this.state;

    // ipcRenderer.send("START_BACKGROUND_VIA_MAIN", {
    //   reportArea: locationList,
    //   selectedIndicators: indicatorList,
    // });

    ipcRenderer.send("FAKE_BACKGROUND_VIA_MAIN");
  }

  render() {
    const { page } = this.props;
    const {
      locationList,
      indicatorList,
      fileName,
      filePath,
      progress,
      progressDialog,
      invalidStatus
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
          invalidStatus={invalidStatus}
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
};
AppSection.defaultProps = {
  page: 0,
  onPageChange: null,
};

export default AppSection;
