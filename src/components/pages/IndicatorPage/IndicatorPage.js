import React from "react";
import PropTypes from "prop-types";
import SectionAccordion from "./subcomponents/SectionAccordion";
import CheckBoxLabel from "./subcomponents/CheckBoxLabel";
import customTables from "../../../assets/data/customTables.json";
import "../../css/IndicatorPage.css";

class IndicatorPage extends React.Component {
  constructor(props) {
    super(props);

    let cbStates = {};
    cbStates.all = false;
    for (let i = 0; i < customTables.length; i += 1) {
      cbStates[`${i}`] = {};
      cbStates[`${i}`]["-1"] = false;
      for (let j = 0; j < customTables[i].SectionTables.length; j += 1) {
        cbStates[`${i}`][`${j}`] = false;
      }
    }

    this.state = {
      checkBoxStates: cbStates,
    };

    this.sectionAccordions = [];

    this.handleTableChange = this.handleTableChange.bind(this);
    this.handleStateChange = this.handleStateChange.bind(this);
    this.onAllBoxClicked = this.onAllBoxClicked.bind(this);
  }

  componentDidMount() {
    const { indicatorList } = this.props;
    // TODO: Implement persistent indicator selection display
    // indicatorList.forEach((indicator) => {
    //   const index = indicator.indicatorIdx;
    //   document.getElementById(index).checked = true;
    //   this.info[index].checked = true;
    // });
  }

  handleTableChange(sid, tid, checked) {
    const { onAddIndicator, onRemoveIndicator } = this.props;

    if (checked) {
      const tableName = customTables[sid].SectionTables[tid].TableName;
      onAddIndicator(sid, tid, tableName);
    } else {
      onRemoveIndicator(sid, tid);
    }
  }

  handleStateChange(id, checked) {
    const { checkBoxStates } = this.state;

    const tmpIDs = id.split(".");
    const sid = parseInt(tmpIDs[0], 10);
    const tid = parseInt(tmpIDs[1], 10);

    if (tid === -1) {
      if (sid === -1) {
        // All Indicators checkbox clicked. Change all checkboxes to match
        checkBoxStates.all = checked
      } else {
        // Section checkbox clicked. Change all section checkboxes to match
        checkBoxStates[sid][tid] = checked

        let allChecked = true;
        for (let i = 0; i < customTables.length; i += 1) {
          if (!checkBoxStates[i]["-1"]) {
            allChecked = false;
          }
        }

        if (allChecked !== checkBoxStates.all) {
          this.handleStateChange("-1.-1", allChecked);
        }
      }
    } else {
      // Indicator checkbox was clicked. Change checkbox to match
      checkBoxStates[sid][tid] = checked
      this.handleTableChange(sid, tid, checked)
    }

    this.setState({ checkBoxStates });
  }

  onAllBoxClicked(event) {
    const { checkBoxStates } = this.state;

    for (let i = 0; i < customTables.length; i += 1) {
      if (checkBoxStates[i]["-1"] !== event.target.checked) {
        checkBoxStates[i]["-1"] = event.target.checked;
      }
      for (let j = 0; j < customTables[i].SectionTables.length; j += 1) {
        if (checkBoxStates[i][j] !== event.target.checked) {
          this.handleStateChange(`${i}.${j}`, event.target.checked)
        }
      }
    }

    this.handleStateChange("-1.-1", event.target.checked)
  }

  render() {
    const { checkBoxStates } = this.state;
    this.sectionAccordions = [];

    for (let i = 0; i < customTables.length; i += 1) {
      const customSection = customTables[i];
      this.sectionAccordions.push(
        <SectionAccordion
          key={`${i}`}
          sid={`${i}`}
          sectionInfo={customSection}
          sectionStates={checkBoxStates[i]}
          handleStateChange={this.handleStateChange}
        />,
      );
    }

    return (
      <div id="IndicatorPage">
        <CheckBoxLabel id="-1.-1" name="All Tables" checked={checkBoxStates.all} onClick={this.onAllBoxClicked} />
        {this.sectionAccordions}
      </div>
    );
  }
}

IndicatorPage.propTypes = {
  indicatorList: PropTypes.arrayOf(
    PropTypes.shape({
      sectionIdx: PropTypes.number,
      tableIdx: PropTypes.number,
      tableName: PropTypes.string,
    }),
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
