import React from "react";
import PropTypes from "prop-types";
import Button from "react-bootstrap/Button";
import Accordion from "react-bootstrap/Accordion";
import Card from "react-bootstrap/Card";
import SectionAccordion from "./subcomponents/SectionAccordion";
import CheckBoxLabel from "./subcomponents/CheckBoxLabel";
import customTables from "../../../assets/data/customTables.json";
import "../../css/IndicatorPage.css";

class IndicatorPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};

    this.sectionAccordions = [];
    // info = {
    //   allInfo: {info},
    //   sectionID: {
    //     sectionInfo: {info},
    //     indicators: [
    //       {info},
    //       ...
    //     ]
    //   },
    //   ...
    // }
    this.info = {};

    this.onCheckBoxClicked = this.onCheckBoxClicked.bind(this);

    // build the indicatorAccordion
    this.buildPage();
  }

  componentDidMount() {
    const { indicatorList } = this.props;
    indicatorList.forEach((indicator) => {
      const index = indicator.indicatorIdx;
      document.getElementById(index).checked = true;
      this.info[index].checked = true;
    });
  }

  onCheckBoxClicked(event) {
    const id = parseInt(event.target.id.substring(3, event.target.id.length), 10);
    const { sid, tid } = this.info[id];
    const { onAddIndicator, onRemoveIndicator } = this.props;

    this.info[id].checked = !this.info[id].checked;
    document.getElementById(event.target.id).checked = this.info[
      id
    ].checked;

    if (tid === -1) {
      if (sid === -1) {
        console.log("all")
      } else {
        console.log("section")
        const sectionID = sid;
        let tmpID = id;
        while (this.info[tmpID].sid === sectionID && tmpID < this.info.length) {
          if (this.info[tmpID].checked !== this.info[id].checked) {
            this.info[tmpID].checked = this.info[id].checked;
            document.getElementById(`cb-${tmpID}`).checked = this.info[
              id
            ].checked;
          }
          tmpID += 1;
        }
      }
    } else {
      if (this.info[id].checked) {
        onAddIndicator(id, sid, tid);
      } else {
        onRemoveIndicator(id, sid, tid);
      }
      console.log("else")
    }
  }

  buildPage() {
    // build the indicator accordion
    let i;
    let j;
    let checkboxID = 0;

    // build the allBox Info
    let allInfo = {};
    allInfo.name = "All Indicators";
    allInfo.id = `cb-${checkboxID.toString()}`
    allInfo.sid = -1;
    allInfo.tid = -1;
    allInfo.checked = false;
    this.info.allInfo = allInfo;

    checkboxID += 1;

    for (i = 0; i < customTables.length; i += 1) {
      const indicatorSection = customTables[i];
      const sectionID = checkboxID;
      this.info[sectionID] = {};
      this.info[sectionID].indicators = [];

      // build a sectionBox Info
      const sectionInfo = {};
      sectionInfo.name = indicatorSection.SectionName;
      sectionInfo.id = `cb-${checkboxID.toString()}`
      sectionInfo.sid = i;
      sectionInfo.tid = -1;
      sectionInfo.checked = false;
      this.info[sectionID].sectionInfo = sectionInfo;
      checkboxID += 1;

      for (j = 0; j < indicatorSection.Tables.length; j += 1) {
        const indicator = indicatorSection.Tables[j];

        // build a indicatorBox Info
        let indicatorInfo = {};
        indicatorInfo.name = indicator.TableName;
        indicatorInfo.id = `cb-${checkboxID.toString()}`
        indicatorInfo.sid = i;
        indicatorInfo.tid = j;
        indicatorInfo.checked = false;
        this.info[sectionID].indicators.push(indicatorInfo);

        checkboxID += 1;
      }

      // build this sectionBox
      this.sectionAccordions.push(
        <SectionAccordion
          sectionInfo={this.info[sectionID].sectionInfo}
          indicators={this.info[sectionID].indicators}
        />
      );
    }
  }

  render() {
    return (
      <div id="IndicatorPage">
        <CheckBoxLabel info={this.info.allInfo} onCheckBoxClicked={this.onCheckBoxClicked} />
        {this.sectionAccordions}
      </div>
    );
  }
}

IndicatorPage.propTypes = {
  indicatorList: PropTypes.arrayOf(
    PropTypes.shape({
      indicatorIdx: PropTypes.number,
      sectionIdx: PropTypes.number,
      tableIdx: PropTypes.number,
    })
  ),
  onAddIndicator: PropTypes.func,
  onRemoveIndicator: PropTypes.func,
};
IndicatorPage.defaultProps = {
  indicatorList: null,
  onAddIndicator: null,
  onRemoveIndicator: null,
};

export default IndicatorPage;
