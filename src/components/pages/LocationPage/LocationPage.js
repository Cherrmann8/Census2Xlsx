import React from "react";
import PropTypes from "prop-types";
import Button from "react-bootstrap/Button";
import LocationLevelButtons from "./subcomponents/LocationLevelButtons";
import SelectorTable from "./subcomponents/SelectorTable";
import SelectionTable from "./subcomponents/SelectionTable";
import locations from "../../../assets/data/locations.json";
import "../../css/LocationPage.css";

class LocationPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      level: "State",
      activeList: "0",
      activePrimaryItem: "",
      activeSecondaryItem: "",
      activeSelectionItem: "",
      primaryTitle: "Select a state:",
      secondaryTitle: "Select a state above",
      stateIdx: -1,
      countyIdx: -1,
      placeIdx: -1,
      locationIdx: -1,
    };

    this.selectionTable = React.createRef();

    this.handleLevelChange = this.handleLevelChange.bind(this);
    this.handleOpenSecondary = this.handleOpenSecondary.bind(this);
    this.handleCloseSecondary = this.handleCloseSecondary.bind(this);
    this.handleAddClick = this.handleAddClick.bind(this);
    this.handleRemoveClick = this.handleRemoveClick.bind(this);
    this.setStateIdx = this.setStateIdx.bind(this);
    this.setCountyIdx = this.setCountyIdx.bind(this);
    this.setPlaceIdx = this.setPlaceIdx.bind(this);
    this.setLocationIdx = this.setLocationIdx.bind(this);
  }

  componentDidMount() {
    // rebuild the selectionList in SelectionTable when this page is mounted
    this.selectionTable.current.buildSelectionTable();
    this.selectionTable.current.forceUpdate();
    document.addEventListener("click", this.handleClick);
  }

  componentWillUnmount() {
    document.removeEventListener("click", this.handleClick);
  }

  handleClick = (e) => {
    const { level } = this.state;
    let selectorClicked = false;
    let selectionClicked = false;

    e.path.forEach((element) => {
      if (element.id === "SelectorTable") {
        selectorClicked = true;
      } else if (element.id === "SelectionTable") {
        selectionClicked = true;
      }
    });

    if (selectorClicked && !selectionClicked) {
      this.setState({
        activeSelectionItem: "",
        locationIdx: -1,
      });
    } else if (!selectorClicked && selectionClicked) {
      if (level === "State") {
        this.setState({
          activePrimaryItem: "",
          stateIdx: -1,
        });
      } else {
        this.setState({
          activeSecondaryItem: "",
          countyIdx: -1,
          placeIdx: -1,
        });
      }
    }
  };

  handleLevelChange(newLevel) {
    const { activeList } = this.state;
    if (activeList !== "0") {
      this.handleCloseSecondary();
    }

    this.setState({
      level: newLevel,
      activeList: "0",
      primaryTitle: "Select a state:",
      secondaryTitle: "Select a state above",
      stateIdx: -1,
      countyIdx: -1,
      placeIdx: -1,
    });
  }

  handleOpenSecondary(stateName) {
    const { level } = this.state;

    let tmpSecondaryTitle;
    if (level === "County") {
      tmpSecondaryTitle = "Select a county";
    } else if (level === "Place") {
      tmpSecondaryTitle = "Select a place";
    }

    this.setState({
      activeList: "1",
      primaryTitle: `State selected: ${stateName}`,
      secondaryTitle: tmpSecondaryTitle,
    });
  }

  handleCloseSecondary() {
    this.setState({
      activeList: "0",
      primaryTitle: "Select a state:",
      secondaryTitle: "Select a state above",
      stateIdx: -1,
      countyIdx: -1,
      placeIdx: -1,
    });
  }

  handleAddClick() {
    const { onAddLocation } = this.props;
    const {
      level,
      stateIdx,
      countyIdx,
      placeIdx,
    } = this.state;

    if (stateIdx !== -1) {
      if (level === "State") {
        onAddLocation(
          locations[stateIdx].StateName,
          "0",
          locations[stateIdx].StateID,
          "-1",
        );
        this.selectionTable.current.buildSelectionTable();
      } else if (countyIdx !== -1 && level === "County") {
        onAddLocation(
          `${locations[stateIdx].Counties[countyIdx].CountyName}, ${locations[stateIdx].StateName}`,
          "1",
          locations[stateIdx].StateID,
          locations[stateIdx].Counties[countyIdx].CountyID,
        );
        this.selectionTable.current.buildSelectionTable();
      } else if (placeIdx !== -1 && level === "Place") {
        onAddLocation(
          `${locations[stateIdx].Places[placeIdx].PlaceName}, ${locations[stateIdx].StateName}`,
          "2",
          locations[stateIdx].StateID,
          locations[stateIdx].Places[placeIdx].PlaceID,
        );
        this.selectionTable.current.buildSelectionTable();
      }
    }
  }

  handleRemoveClick() {
    const { onRemoveLocation } = this.props;
    const { locationIdx } = this.state;

    if (locationIdx !== -1) {
      onRemoveLocation(locationIdx);
      this.selectionTable.current.buildSelectionTable();
    }
  }

  setStateIdx(newIdx) {
    this.setState({ stateIdx: parseInt(newIdx, 10) });
    this.setState({ activePrimaryItem: newIdx, activeSecondaryItem: "" });
  }

  setCountyIdx(newIdx) {
    this.setState({ countyIdx: parseInt(newIdx, 10) });
    this.setState({ activeSecondaryItem: newIdx, activePrimaryItem: "" });
  }

  setPlaceIdx(newIdx) {
    this.setState({ placeIdx: parseInt(newIdx, 10) });
    this.setState({ activeSecondaryItem: newIdx, activePrimaryItem: "" });
  }

  setLocationIdx(newIdx) {
    this.setState({ locationIdx: newIdx });
    this.setState({ activeSelectionItem: newIdx });
  }

  render() {
    const { locationList } = this.props;
    const {
      level,
      activeList,
      primaryTitle,
      secondaryTitle,
      activePrimaryItem,
      activeSecondaryItem,
      activeSelectionItem,
    } = this.state;

    return (
      <div className="LocationPage">
        <LocationLevelButtons onLevelChange={this.handleLevelChange} />
        <div className="LocationTables">
          <SelectorTable
            level={level}
            activeList={activeList}
            primaryTitle={primaryTitle}
            secondaryTitle={secondaryTitle}
            onOpenSecondary={this.handleOpenSecondary}
            onCloseSecondary={this.handleCloseSecondary}
            onDoubleClick={this.handleAddClick}
            activePrimaryItem={activePrimaryItem}
            activeSecondaryItem={activeSecondaryItem}
            setStateIdx={this.setStateIdx}
            setCountyIdx={this.setCountyIdx}
            setPlaceIdx={this.setPlaceIdx}
            locations={locations}
          />
          <div className="LocationTableButtons">
            <Button id="AddLocationButtton" onClick={this.handleAddClick}>
              Add
            </Button>
            <Button id="RemoveLocationButtton" onClick={this.handleRemoveClick}>
              Remove
            </Button>
          </div>
          <SelectionTable
            ref={this.selectionTable}
            locationList={locationList}
            activeSelectionItem={activeSelectionItem}
            setLocationIdx={this.setLocationIdx}
          />
        </div>
      </div>
    );
  }
}

LocationPage.propTypes = {
  locationList: PropTypes.arrayOf(
    PropTypes.shape({
      locationName: PropTypes.string,
      geographicLevel: PropTypes.string,
      primaryID: PropTypes.string,
      secondaryID: PropTypes.string,
    }),
  ),
  onAddLocation: PropTypes.func,
  onRemoveLocation: PropTypes.func,
};
LocationPage.defaultProps = {
  locationList: null,
  onAddLocation: null,
  onRemoveLocation: null,
};

export default LocationPage;
