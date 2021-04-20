import React from "react";
import PropTypes from "prop-types";
import Button from "react-bootstrap/Button";
import Accordion from "react-bootstrap/Accordion";
import Card from "react-bootstrap/Card";
import ListGroup from "react-bootstrap/ListGroup";
import InputGroup from "react-bootstrap/InputGroup";
import FormControl from "react-bootstrap/FormControl";
import { Col, Form, Row } from "react-bootstrap";
import "../../css/ConfirmationPage.css";

const electron = window.require("electron");
const { ipcRenderer } = electron;

class ConfirmationPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};

    const { locationList, indicatorList } = this.props;
    this.lList = [];
    this.iList = [];

    let itemID = 0;
    locationList.forEach((location) => {
      this.lList.push(
        <ListGroup.Item action={false} eventKey={itemID} key={itemID}>
          {location.locationName}
        </ListGroup.Item>,
      );
      itemID += 1;
    });

    itemID = 0;
    indicatorList.forEach((indicator) => {
      this.iList.push(
        <ListGroup.Item eventKey={itemID} key={itemID}>
          {
            indicator.tableName
          }
        </ListGroup.Item>,
      );
      itemID += 1;
    });

    this.dialog = this.dialog.bind(this);
  }

  onNameChange = (e) => {
    const { onFileNameChange } = this.props;
    onFileNameChange(e.target.value);
  }

  dialog() {
    const { locationList } = this.props;
    ipcRenderer.send("START_DIALOG");
  }

  render() {
    const {
      fileName,
      filePath,
      invalidFileName,
      invalidFilePath,
    } = this.props;

    return (
      <div className="ConfirmationPage">
        <div className="ConfirmationTables">
          <Accordion id="locationConfTable" defaultActiveKey="0">
            <Card>
              <Card.Header id="ListHeader">
                <Accordion.Toggle as={Card.Header} variant="link" eventKey="0">
                  Report Area
                </Accordion.Toggle>
              </Card.Header>
              <Accordion.Collapse eventKey="0">
                <Card.Body id="ConfirmationList">
                  <ListGroup variant="flush" activeKey="-1" id="ConfLocListGroup">
                    {this.lList}
                  </ListGroup>
                </Card.Body>
              </Accordion.Collapse>
            </Card>
          </Accordion>
          <Accordion id="indicatorConfTable" defaultActiveKey="0">
            <Card>
              <Card.Header id="ListHeader">
                <Accordion.Toggle as={Card.Header} variant="link" eventKey="0">
                  Selected Tables
                </Accordion.Toggle>
              </Card.Header>
              <Accordion.Collapse eventKey="0">
                <Card.Body id="ConfirmationList">
                  <ListGroup variant="flush" activeKey="-1">
                    {this.iList}
                  </ListGroup>
                </Card.Body>
              </Accordion.Collapse>
            </Card>
          </Accordion>
        </div>
        <Form id="ConfirmationForm">
          <Form.Group as={Row}>
            <Form.Label column sm={1} htmlFor="fileName">Name:</Form.Label>
            <Col sm={11}>
              <InputGroup hasValidation>
                <FormControl
                  required
                  id="fileName"
                  placeholder="Enter a file name..."
                  onChange={this.onNameChange}
                  isInvalid={invalidFileName}
                />
                <InputGroup.Append>
                  <InputGroup.Text>.xlsx</InputGroup.Text>
                </InputGroup.Append>
                <Form.Control.Feedback type="invalid">
                  Please choose a file name
                </Form.Control.Feedback>
              </InputGroup>
            </Col>
          </Form.Group>
          <Form.Group as={Row}>
            <Form.Label column sm={1} htmlFor="filePath">Path:</Form.Label>
            <Col sm={11}>
              <InputGroup hasValidation>
                <FormControl
                  required
                  id="filePath"
                  placeholder={filePath}
                  value={filePath}
                  isInvalid={false}
                />
                <InputGroup.Append>
                  <Button onClick={this.dialog}>Choose...</Button>
                </InputGroup.Append>
                <Form.Control.Feedback type="invalid">
                  Please choose a file path
                </Form.Control.Feedback>
              </InputGroup>
            </Col>
          </Form.Group>
        </Form>
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
  fileName: PropTypes.string,
  filePath: PropTypes.string,
  invalidFileName: PropTypes.bool,
  invalidFilePath: PropTypes.bool,
  onFileNameChange: PropTypes.func,
};
ConfirmationPage.defaultProps = {
  locationList: null,
  indicatorList: null,
  fileName: "",
  filePath: "",
  invalidFileName: false,
  invalidFilePath: false,
  onFileNameChange: null,
};

export default ConfirmationPage;
