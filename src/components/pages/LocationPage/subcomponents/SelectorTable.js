import React from "react";
import PropTypes from "prop-types";
import Accordion from "react-bootstrap/Accordion";
import Card from "react-bootstrap/Card";
import Button from "react-bootstrap/Button";
import FormControl from "react-bootstrap/FormControl";
import ListGroup from "react-bootstrap/ListGroup";
import { Container, Row } from "react-bootstrap";

class SelectorTable extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};

    // put each state name into the listgroup
    this.primaryList = [];
    this.filteredPrimaryList = [];
    this.secondaryList = [];
    this.filteredSecondaryList = [];
    this.hideAll = true;
    const { locations } = this.props;
    let itemID = 0;
    locations.forEach((location) => {
      this.primaryList.push(
        <ListGroup.Item
          action
          eventKey={itemID}
          key={itemID}
          onClick={(e) => this.onPrimaryListClick(e)}
        >
          {location.StateName}
        </ListGroup.Item>
      );
      itemID += 1;
    });
    this.filteredPrimaryList = this.primaryList;

    this.formFilter = React.createRef();

    this.handleFilterChange = this.handleFilterChange.bind(this);
    this.handleResetClick = this.handleResetClick.bind(this);
    this.onSecondayListClick = this.onSecondaryListClick.bind(this);
    this.onPrimaryListClick = this.onPrimaryListClick.bind(this);
  }

  componentDidMount() {
    window.addEventListener("resize", this.updateDimensions.bind(this));
    this.updateDimensions();
  }

  componentDidUpdate() {
    this.updateDimensions();
  }

  componentWillUnmount() {
    window.removeEventListener("resize", this.updateDimensions());
  }

  handleFilterReset() {
    this.formFilter.current.value = "";
    this.filteredPrimaryList = this.primaryList;
  }

  handleFilterChange(event) {
    const { activeList } = this.props;
    const filter = event.target.value.toUpperCase();

    if (activeList === "0") {
      this.filteredPrimaryList = [];
      this.primaryList.forEach((location) => {
        const item = location.props.children.toUpperCase();
        if (item.indexOf(filter) >= 0) {
          this.filteredPrimaryList.push(location);
        }
      });
    } else {
      this.filteredSecondaryList = [];
      this.secondaryList.forEach((location) => {
        const item = location.props.children.toUpperCase();
        if (item.indexOf(filter) >= 0) {
          this.filteredSecondaryList.push(location);
        }
      });
    }
    this.forceUpdate();
  }

  handleResetClick() {
    const { onCloseSecondary } = this.props;
    this.handleFilterReset();
    onCloseSecondary();
  }

  onSecondaryListClick(event) {
    const { level, setCountyIdx, setPlaceIdx, onDoubleClick } = this.props;

    const tmpSecondaryIdx = event.target.attributes[0].value;

    if (level === "County") {
      setCountyIdx(tmpSecondaryIdx);
    } else if (level === "Place") {
      setPlaceIdx(tmpSecondaryIdx);
    }

    if (event.detail === 2) {
      onDoubleClick();
    }
  }

  onPrimaryListClick(event) {
    const tmpStateIdx = event.target.attributes[0].value;
    const { level, onOpenSecondary, setStateIdx, onDoubleClick } = this.props;

    // set the stateIdx
    setStateIdx(tmpStateIdx);

    if (level !== "State") {
      const { locations } = this.props;

      // change the primaryList title
      onOpenSecondary(locations[tmpStateIdx].StateName);
      this.handleFilterReset();

      // create secondaryList
      this.secondaryList = [];
      let tmpSecondary = null;
      let itemID = 0;
      if (level === "County") {
        tmpSecondary = locations[tmpStateIdx].Counties;
        tmpSecondary.forEach((secondary) => {
          this.secondaryList.push(
            <ListGroup.Item
              action
              eventKey={itemID}
              key={itemID}
              onClick={(e) => this.onSecondaryListClick(e)}
            >
              {secondary.CountyName}
            </ListGroup.Item>,
          );
          itemID += 1;
        });
      } else if (level === "Place") {
        tmpSecondary = locations[tmpStateIdx].Places;
        tmpSecondary.forEach((secondary) => {
          this.secondaryList.push(
            <ListGroup.Item
              action
              eventKey={itemID}
              key={itemID}
              onClick={(e) => this.onSecondaryListClick(e)}
            >
              {secondary.PlaceName}
            </ListGroup.Item>,
          );
          itemID += 1;
        });
      }
      this.filteredSecondaryList = this.secondaryList;
    } else {
      if (event.detail === 2) {
        onDoubleClick();
      }
    }
  }

  updateDimensions() {
    const { level } = this.props;
    // console.log("---")
    const SelectorHeader = document.getElementById("SelectorAccordionHeader").clientHeight;
    // console.log(SelectorHeader);
    // const SelectorBody = document.getElementById("SelectorList").clientHeight;
    // console.log(SelectorBody);

    const SelectionHeader = document.getElementById("SelectionAccordionHeader").clientHeight;
    // console.log(SelectionHeader);
    const SelectionBody = document.getElementById("SelectionList").clientHeight;
    // console.log(SelectionBody);

    const targetHeight = (SelectionHeader + SelectionBody) - SelectorHeader;
    // console.log(targetHeight);
    document.getElementById("SelectorList").style.height = `${targetHeight}px`;
  }

  render() {
    // build the selectorTable
    const {
      level,
      activeList,
      primaryTitle,
      secondaryTitle,
      activePrimaryItem,
      activeSecondaryItem,
    } = this.props;

    let resetStateButton = (
      <Button id="ResetStateButton" onClick={this.handleResetClick}>
        Reset
      </Button>
    );

    let listGroupItems;
    let activeItem;
    if (activeList === "0") {
      listGroupItems = this.filteredPrimaryList;
      activeItem = activePrimaryItem;
    } else {
      listGroupItems = this.filteredSecondaryList;
      activeItem = activeSecondaryItem;
    }

    return (
      <div id="SelectorTable">
        <Accordion defaultActiveKey="0" activeKey="0">
          <Card>
            <Card.Header id="SelectorAccordionHeader">
              <Accordion.Toggle as="h6" eventKey="0">
                <div id="SelectorHeader">
                  <div id="SelectorPrimaryHeader">
                    {primaryTitle}
                    {activeList !== "0" ? resetStateButton : null}
                  </div>
                  {activeList !== "0" ? secondaryTitle : null}
                  <FormControl
                    ref={this.formFilter}
                    onKeyUp={(e) => this.handleFilterChange(e)}
                    placeholder="filter..."
                  />
                </div>
              </Accordion.Toggle>
            </Card.Header>
            <Accordion.Collapse eventKey="0">
              <Card.Body id="SelectorList">
                <ListGroup variant="flush" activeKey={activeItem}>
                  {listGroupItems}
                </ListGroup>
              </Card.Body>
            </Accordion.Collapse>
          </Card>
        </Accordion>
      </div>
    );
  }
}

SelectorTable.propTypes = {
  level: PropTypes.string,
  activeList: PropTypes.string,
  primaryTitle: PropTypes.string,
  secondaryTitle: PropTypes.string,
  onOpenSecondary: PropTypes.func,
  onCloseSecondary: PropTypes.func,
  onDoubleClick: PropTypes.func,
  activePrimaryItem: PropTypes.string,
  activeSecondaryItem: PropTypes.string,
  setStateIdx: PropTypes.func,
  setCountyIdx: PropTypes.func,
  setPlaceIdx: PropTypes.func,
  locations: PropTypes.arrayOf(
    PropTypes.shape({
      StateName: PropTypes.string,
      StateID: PropTypes.string,
      Counties: PropTypes.arrayOf(
        PropTypes.shape({
          CountyName: PropTypes.string,
          CountyID: PropTypes.string,
        }),
      ),
      Places: PropTypes.arrayOf(
        PropTypes.shape({
          PlaceName: PropTypes.string,
          PlaceID: PropTypes.string,
        }),
      ),
    }),
  ),
};
SelectorTable.defaultProps = {
  level: "State",
  activeList: "0",
  primaryTitle: "Select a state",
  secondaryTitle: "Select a state above",
  onOpenSecondary: null,
  onCloseSecondary: null,
  onDoubleClick: null,
  activePrimaryItem: null,
  activeSecondaryItem: null,
  setStateIdx: null,
  setCountyIdx: null,
  setPlaceIdx: null,
  locations: null,
};

export default SelectorTable;
