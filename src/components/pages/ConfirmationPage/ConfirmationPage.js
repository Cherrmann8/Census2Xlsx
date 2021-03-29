import React from "react";
import PropTypes from "prop-types";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Accordion from "react-bootstrap/Accordion";
import Card from "react-bootstrap/Card";
import ListGroup from "react-bootstrap/ListGroup";
import dataTables from "../../../assets/data/customTables.json";
import "../../css/ConfirmationPage.css";

const electron = window.require("electron");
const { ipcRenderer } = electron;

class ConfirmationPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};

    this.lList = [];
    this.iList = [];

    this.dialogue = this.dialogue.bind(this);

    ipcRenderer.on("RETURN_DIALOG", (event, args) => {
      console.log(args);
    });
  }

  dialogue() {
    // const electron = window.require("electron");
    // const { dialog } = electron;
    const { locationList } = this.props;
    console.log("clicked!");
    // console.log(dialog.showOpenDialog(electron.renderer.Remote.getCurrentWindow(), {}))

    ipcRenderer.send("START_DIALOG");
  }

  render() {
    const { locationList, indicatorList } = this.props;

    let itemID = 0;
    locationList.forEach((location) => {
      this.lList.push(
        <ListGroup.Item action eventKey={itemID} key={itemID}>
          {location.locationName}
        </ListGroup.Item>,
      );
      itemID += 1;
    });

    itemID = 0;
    indicatorList.forEach((indicator) => {
      this.iList.push(
        <ListGroup.Item action eventKey={itemID} key={itemID}>
          {
            indicator.tableName
          }
        </ListGroup.Item>,
      );
      itemID += 1;
    });

    return (
      <div className="ConfirmationPage">
        <div className="ConfirmationTables">
          <Accordion defaultActiveKey="0">
            <Card>
              <Card.Header id="ListHeader">
                <Accordion.Toggle as={Card.Header} variant="link" eventKey="0">
                  Report Area
                </Accordion.Toggle>
              </Card.Header>
              <Accordion.Collapse eventKey="0">
                <Card.Body id="ConfirmationList">
                  <ListGroup variant="flush">
                    {this.lList}
                  </ListGroup>
                </Card.Body>
              </Accordion.Collapse>
            </Card>
          </Accordion>
          <Accordion defaultActiveKey="0">
            <Card>
              <Card.Header id="ListHeader">
                <Accordion.Toggle as={Card.Header} variant="link" eventKey="0">
                  Selected Tables
                </Accordion.Toggle>
              </Card.Header>
              <Accordion.Collapse eventKey="0">
                <Card.Body id="ConfirmationList">
                  <ListGroup variant="flush">
                    {this.iList}
                  </ListGroup>
                </Card.Body>
              </Accordion.Collapse>
            </Card>
          </Accordion>
        </div>
        <Form.File
          name="file"
          label="Save as"
        />
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
    }),
  ),
  indicatorList: PropTypes.arrayOf(
    PropTypes.shape({
      indicatorIdx: PropTypes.number,
      sectionIdx: PropTypes.number,
      tableIdx: PropTypes.number,
    }),
  ),
};
ConfirmationPage.defaultProps = {
  locationList: null,
  indicatorList: null,
};

export default ConfirmationPage;
