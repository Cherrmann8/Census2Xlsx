import React from "react";
import PropTypes from "prop-types";
import Accordion from "react-bootstrap/Accordion";
import Card from "react-bootstrap/Card";
import CheckBoxLabel from "./CheckBoxLabel";
import "../../../css/IndicatorPage.css";

class SectionAccordion extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};

    this.onSectionBoxClicked = this.onSectionBoxClicked.bind(this);
    this.onTableBoxClicked = this.onTableBoxClicked.bind(this);
  }

  onSectionBoxClicked(event) {
    const { sid, sectionInfo, sectionStates, handleStateChange } = this.props;
    handleStateChange(event.target.id, event.target.checked);

    for (let i = 0; i < sectionInfo.SectionTables.length; i += 1) {
      if (sectionStates[i] !== event.target.checked) {
        handleStateChange(`${sid}.${i}`, event.target.checked);
      }
    }
  }

  onTableBoxClicked(event) {
    const { sid, sectionInfo, sectionStates, handleStateChange } = this.props;
    handleStateChange(event.target.id, event.target.checked);

    let sectionChecked = true;
    for (let i = 0; i < sectionInfo.SectionTables.length; i += 1) {
      if (!sectionStates[i]) {
        sectionChecked = false;
      }
    }

    if (sectionChecked !== sectionStates["-1"]) {
      handleStateChange(`${sid}.-1`, sectionChecked);
    }
  }

  render() {
    const { sid, sectionInfo, sectionStates } = this.props;
    const sectionTables = [];
    for (let i = 0; i < sectionInfo.SectionTables.length; i += 1) {
      const table = sectionInfo.SectionTables[i];
      sectionTables.push(
        <CheckBoxLabel
          id={`${sid}.${i}`}
          name={table.TableName}
          checked={sectionStates[i]}
          onClick={this.onTableBoxClicked}
        />,
      );
    }

    return (
      <div className="SectionAccordion">
        <Accordion defaultActiveKey={sid}>
          <Card>
            <Card.Header id="indicatorHeader">
              <Accordion.Toggle as={Card.Header} variant="link" eventKey={sid}>
                <div>
                  <label htmlFor={`${sid}.-1`}>
                    <input
                      type="checkbox"
                      name={sectionInfo.SectionName}
                      id={`${sid}.-1`}
                      checked={sectionStates["-1"]}
                      onChange={(e) => this.onSectionBoxClicked(e)}
                    />
                    {sectionInfo.SectionName}
                  </label>
                </div>
              </Accordion.Toggle>
            </Card.Header>
            <Accordion.Collapse eventKey={sid}>
              <Card.Body>{sectionTables}</Card.Body>
            </Accordion.Collapse>
          </Card>
        </Accordion>
      </div>
    );
  }
}

SectionAccordion.propTypes = {
  sid: PropTypes.string,
  sectionInfo: PropTypes.shape({
    SectionName: PropTypes.string,
    SectionTables: PropTypes.arrayOf(
      PropTypes.shape({
        TableName: PropTypes.string,
        TableIndicators: PropTypes.arrayOf(
          PropTypes.shape({
            IndicatorName: PropTypes.string,
            IndicatorFormula: PropTypes.arrayOf(
              PropTypes.string,
            ),
          }),
        ),
      }),
    ),
  }),
  sectionStates: PropTypes.arrayOf(
    PropTypes.bool,
  ),
  handleStateChange: PropTypes.func,
};
SectionAccordion.defaultProps = {
  sid: null,
  sectionInfo: null,
  sectionStates: null,
  handleStateChange: null,
};

export default SectionAccordion;
