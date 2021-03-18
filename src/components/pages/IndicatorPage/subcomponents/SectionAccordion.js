import React from "react";
import PropTypes from "prop-types";
import Accordion from "react-bootstrap/Accordion";
import Card from "react-bootstrap/Card";
import "../../../css/IndicatorPage.css";
import CheckBoxLabel from "./CheckBoxLabel";

class SectionAccordion extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    const { sectionInfo, indicators } = this.props
    const indicatorBoxes = [];
    indicators.forEach((indicator) => {
      indicatorBoxes.push(<CheckBoxLabel info={indicator} />)
    });

    return (
      <div className="SectionAccordion">
        <Accordion defaultActiveKey={sectionInfo.id}>
          <Card>
            <Card.Header id="indicatorHeader">
              <Accordion.Toggle as={Card.Header} variant="link" eventKey={sectionInfo.id}>
                <div>
                  <label htmlFor={sectionInfo.id}>
                    <input
                      type="checkbox"
                      name={sectionInfo.name}
                      id={sectionInfo.id}
                      onChange={(e) => this.onCheckBoxClicked(e)}
                    />
                    {sectionInfo.name}
                  </label>
                </div>
              </Accordion.Toggle>
            </Card.Header>
            <Accordion.Collapse eventKey={sectionInfo.id}>
              <Card.Body>{indicatorBoxes}</Card.Body>
            </Accordion.Collapse>
          </Card>
        </Accordion>
      </div>
    );
  }
}

SectionAccordion.propTypes = {
  sectionInfo: PropTypes.shape({
    name: PropTypes.string,
    id: PropTypes.string,
    sid: PropTypes.number,
    tid: PropTypes.number,
  }),
  indicators: PropTypes.arrayOf(
    PropTypes.shape({
      name: PropTypes.string,
      id: PropTypes.string,
      sid: PropTypes.number,
      tid: PropTypes.number,
    }),
  ),
  // onSectionClicked: PropTypes.func,
};
SectionAccordion.defaultProps = {
  sectionInfo: null,
  indicators: null,
  // onSectionClicked: null,
};

export default SectionAccordion;
