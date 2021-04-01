import React from "react";
import PropTypes from "prop-types";
import Accordion from "react-bootstrap/Accordion";
import Card from "react-bootstrap/Card";
import ListGroup from "react-bootstrap/ListGroup";

class SelectionTable extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};

    this.selectionList = [];

    this.buildSelectionTable = this.buildSelectionTable.bind(this);
    this.onLocationListClick = this.onLocationListClick.bind(this);
  }

  onLocationListClick(event) {
    const { setLocationIdx } = this.props;

    const tmpLocationIdx = event.target.attributes[0].value;
    console.log(tmpLocationIdx);

    setLocationIdx(tmpLocationIdx);
  }

  buildSelectionTable() {
    console.log("Building selectionTable");

    const { locationList } = this.props;
    this.selectionList = [];
    let itemID = 0;

    console.log(locationList);

    locationList.forEach((location) => {
      this.selectionList.push(
        <ListGroup.Item
          action
          eventKey={itemID}
          key={itemID}
          onClick={(e) => this.onLocationListClick(e)}
        >
          {location.locationName}
        </ListGroup.Item>,
      );

      itemID += 1;
    });
  }

  render() {
    const { activeSelectionItem } = this.props;

    return (
      <div id="SelectionTable">
        <Accordion defaultActiveKey="0" activeKey="0">
          <Card>
            <Card.Header id="SelectionAccordionHeader">
              <span>Report Area</span>
            </Card.Header>
            <Accordion.Collapse eventKey="0">
              <Card.Body id="SelectionList">
                <ListGroup variant="flush" activeKey={activeSelectionItem}>{this.selectionList}</ListGroup>
              </Card.Body>
            </Accordion.Collapse>
          </Card>
        </Accordion>
      </div>
    );
  }
}

SelectionTable.propTypes = {
  locationList: PropTypes.arrayOf(
    PropTypes.shape({
      locationName: PropTypes.string,
      geographicLevel: PropTypes.string,
      primaryID: PropTypes.string,
      secondaryID: PropTypes.string,
    }),
  ),
  activeSelectionItem: PropTypes.string,
  setLocationIdx: PropTypes.func,
};
SelectionTable.defaultProps = {
  locationList: null,
  activeSelectionItem: null,
  setLocationIdx: null,
};

export default SelectionTable;
