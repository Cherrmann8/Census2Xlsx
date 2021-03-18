import React from "react";
import PropTypes from "prop-types";
import Accordion from "react-bootstrap/Accordion";
import Card from "react-bootstrap/Card";
import Button from "react-bootstrap/Button";
import ListGroup from "react-bootstrap/ListGroup";

class SelectorTable extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};

    // put each state name into the listgroup
    this.stateList = [];
    this.secondariesList = [];
    const { locations } = this.props;
    let itemID = 0;
    locations.forEach((location) => {
      this.stateList.push(
        <ListGroup.Item
          action
          eventKey={itemID}
          key={itemID}
          onClick={(e) => this.onStateListClick(e)}
        >
          {location.StateName}
        </ListGroup.Item>,
      );
      itemID += 1;
    });

    this.onSecondariesListClick = this.onSecondariesListClick.bind(this);
    this.onStateListClick = this.onStateListClick.bind(this);
    this.buildSelectorTable = this.buildSelectorTable.bind(this);
  }

  onSecondariesListClick(event) {
    const { level, setCountyIdx, setPlaceIdx } = this.props;

    const tmpSecondaryIdx = event.target.attributes[0].value;
    // console.log(tmpSecondaryIdx)

    if (level === "County") {
      setCountyIdx(tmpSecondaryIdx);
    } else if (level === "Place") {
      setPlaceIdx(tmpSecondaryIdx);
    }
  }

  onStateListClick(event) {
    const tmpStateIdx = event.target.attributes[0].value;
    const { level, onOpenSecondary, setStateIdx } = this.props;

    // set the stateIdx
    setStateIdx(tmpStateIdx);

    if (level !== "State") {
      const { locations } = this.props;

      // change the stateList title
      onOpenSecondary(locations[tmpStateIdx].StateName);

      // create secondaryList
      this.secondariesList = [];
      let tmpSecondaries = null;
      let itemID = 0;
      if (level === "County") {
        tmpSecondaries = locations[tmpStateIdx].Counties;
        tmpSecondaries.forEach((secondary) => {
          this.secondariesList.push(
            <ListGroup.Item
              action
              eventKey={itemID}
              key={itemID}
              onClick={(e) => this.onSecondariesListClick(e)}
            >
              {secondary.CountyName}
            </ListGroup.Item>,
          );
          itemID += 1;
        });
      } else if (level === "Place") {
        tmpSecondaries = locations[tmpStateIdx].Places;
        tmpSecondaries.forEach((secondary) => {
          this.secondariesList.push(
            <ListGroup.Item
              action
              eventKey={itemID}
              key={itemID}
              onClick={(e) => this.onSecondariesListClick(e)}
            >
              {secondary.PlaceName}
            </ListGroup.Item>,
          );
          itemID += 1;
        });
      }
    }
  }

  buildSelectorTable() {
    console.log("Building selectorTable");

    const {
      level,
      activeCard,
      primaryTitle,
      secondaryTitle,
    } = this.props;

    let secondaryCard = null;
    if (level !== "State") {
      secondaryCard = (
        <Card>
          <Card.Header>
            <Accordion.Toggle as="h6" eventKey="1">
              {secondaryTitle}
            </Accordion.Toggle>
          </Card.Header>
          <Accordion.Collapse eventKey="1">
            <Card.Body id="SelectorList">
              <ListGroup variant="flush">{this.secondariesList}</ListGroup>
            </Card.Body>
          </Accordion.Collapse>
        </Card>
      );
    }

    return (
      <Accordion defaultActiveKey={activeCard} activeKey={activeCard}>
        <Card>
          <Card.Header>
            <Accordion.Toggle as="h6" eventKey="0">
              {primaryTitle}
            </Accordion.Toggle>
          </Card.Header>
          <Accordion.Collapse eventKey="0">
            <Card.Body id="SelectorList">
              <ListGroup variant="flush">{this.stateList}</ListGroup>
            </Card.Body>
          </Accordion.Collapse>
        </Card>
        {secondaryCard}
      </Accordion>
    );
  }

  render() {
    // build the selectorTable
    const selectorTable = this.buildSelectorTable();

    return <div id="SelectorTable">{selectorTable}</div>;
  }
}

SelectorTable.propTypes = {
  level: PropTypes.string,
  // activeList: PropTypes.string,
  activeCard: PropTypes.string,
  primaryTitle: PropTypes.string,
  secondaryTitle: PropTypes.string,
  onOpenSecondary: PropTypes.func,
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
    })
  ),
};
SelectorTable.defaultProps = {
  level: "State",
  // activeList: '0',
  activeCard: "0",
  primaryTitle: "Select a state",
  secondaryTitle: "Select a state above",
  onOpenSecondary: null,
  setStateIdx: null,
  setCountyIdx: null,
  setPlaceIdx: null,
  locations: null,
};

export default SelectorTable;
