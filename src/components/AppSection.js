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
      progress: 0,
    };

    this.addLocation = this.addLocation.bind(this);
    this.removeLocation = this.removeLocation.bind(this);
    this.addIndicator = this.addIndicator.bind(this);
    this.removeIndicator = this.removeIndicator.bind(this);
    this.startPythonScript = this.startPythonScript.bind(this);

    const { onPageChange } = this.props;

    ipcRenderer.on("MESSAGE_FROM_BACKGROUND_VIA_MAIN", (event, args) => {
      console.log(args)
      const newProgress = parseFloat(args) * 100;
      this.setState({ progress: newProgress });
      if (newProgress >= 100) {
        onPageChange(1);
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
    const { locationList, indicatorList, progress } = this.state;

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
        />
      );
    } else if (page === 3) {
      section = (
        <LoadingPage progress={progress} onPageMount={this.startPythonScript} />
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
