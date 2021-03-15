import React from "react";
import PropTypes from "prop-types";
import ListGroup from "react-bootstrap/ListGroup";
import dataTables from "../../../assets/data/customTables.json";

class ConfirmationPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};

    this.lList = [];
    this.iList = [];
  }

  render() {
    const { locationList, indicatorList } = this.props;

    let itemID = 0;
    locationList.forEach((location) => {
      this.lList.push(
        <ListGroup.Item action eventKey={itemID} key={itemID}>
          {location.locationName}
        </ListGroup.Item>
      );
      itemID += 1;
    });

    itemID = 0;
    indicatorList.forEach((indicator) => {
      this.iList.push(
        <ListGroup.Item action eventKey={itemID} key={itemID}>
          {
            dataTables[indicator.sectionIdx].Tables[indicator.tableIdx]
              .TableName
          }
        </ListGroup.Item>
      );
      itemID += 1;
    });

    return (
      <div>
        <ListGroup>{this.lList}</ListGroup>
        <ListGroup>{this.iList}</ListGroup>
      </div>
    );
  }
}

ConfirmationPage.propTypes = {
  locationList: PropTypes.arrayOf(
    PropTypes.shape({
      locationName: PropTypes.string,
      geographicLevel: PropTypes.string,
      primaryID: PropTypes.string,
      secondaryID: PropTypes.string,
    })
  ),
  indicatorList: PropTypes.arrayOf(
    PropTypes.shape({
      indicatorIdx: PropTypes.number,
      sectionIdx: PropTypes.number,
      tableIdx: PropTypes.number,
    })
  ),
};
ConfirmationPage.defaultProps = {
  locationList: null,
  indicatorList: null,
};

export default ConfirmationPage;
