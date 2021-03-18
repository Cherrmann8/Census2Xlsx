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

    const { locationList, locations } = this.props;
    this.selectionList = [];
    let itemID = 0;

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
    return (
      <div id="SelectionTable">
        <Accordion defaultActiveKey="0" activeKey="0">
          <Card>
            <Card.Header>
              <h6>Report Area</h6>
            </Card.Header>
            <Accordion.Collapse eventKey="0">
              <Card.Body id="SelectionList">
                <ListGroup variant="flush">{this.selectionList}</ListGroup>
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
  setLocationIdx: PropTypes.func,
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
SelectionTable.defaultProps = {
  locationList: null,
  setLocationIdx: null,
  locations: null,
};

export default SelectionTable;
