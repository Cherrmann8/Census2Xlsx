import React from "react";
import PropTypes from "prop-types";
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
    //   sections: [
    //     {
    //       name,
    //       id,
    //       checked,
    //       indicators: [
    //         {info},
    //         ...
    //       ]
    //     },
    //     ...
    //   ]
    // }
    this.info = {};

    this.handleIndicatorChange = this.handleIndicatorChange.bind(this);
    this.handleSectionChange = this.handleSectionChange.bind(this);
    this.onCheckBoxClicked = this.onCheckBoxClicked.bind(this);

    // build the indicatorAccordion
    this.buildPage();
  }

  componentDidMount() {
    const { indicatorList } = this.props;
    // TODO: Implement persistent indicator selection display
    // indicatorList.forEach((indicator) => {
    //   const index = indicator.indicatorIdx;
    //   document.getElementById(index).checked = true;
    //   this.info[index].checked = true;
    // });
    console.log(indicatorList);
  }

  handleSectionChange(id, sid, checked) {
    this.info.sections[sid].checked = checked;
    document.getElementById(id).checked = checked;
    for (let i = 0; i < this.info.sections[sid].indicators.length; i += 1) {
      if (this.info.sections[sid].indicators[i].checked !== this.info.sections[sid].checked) {
        this.handleIndicatorChange(`cb.${sid}.${i}`, sid, i, this.info.sections[sid].checked);
      }
    }
  }

  handleIndicatorChange(id, sid, tid, checked) {
    const { onAddIndicator, onRemoveIndicator } = this.props;

    this.info.sections[sid].indicators[tid].checked = checked;
    document.getElementById(id).checked = checked;
    if (this.info.sections[sid].indicators[tid].checked) {
      onAddIndicator(sid, tid);
    } else {
      onRemoveIndicator(sid, tid);
    }
  }

  onCheckBoxClicked(event) {
    // Get the section and table IDs from the target ID
    const tmpIDs = event.target.id.split(".");
    const sid = parseInt(tmpIDs[1], 10);
    const tid = parseInt(tmpIDs[2], 10);

    console.log(`${sid}.${tid}`);

    if (tid === -1) {
      if (sid === -1) {
        // All Indicators checkbox clicked. Change all checkboxes to match
        this.info.allInfo.checked = !this.info.allInfo.checked;
        document.getElementById(event.target.id).checked = this.info.allInfo.checked;

        for (let i = 0; i < this.info.sections.length; i += 1) {
          if (this.info.sections[i].checked !== this.info.allInfo.checked) {
            this.handleSectionChange(`cb.${i}.-1`, i, this.info.allInfo.checked);
          }
        }
      } else {
        // Section checkbox clicked. Change all section checkboxes to match
        this.handleSectionChange(event.target.id, sid, !this.info.sections[sid].checked);
      }
    } else {
      // Indicator checkbox was clicked. Change checkbox to match
      this.handleIndicatorChange(
        event.target.id,
        sid,
        tid,
        !this.info.sections[sid].indicators[tid].checked,
      );
    }
  }

  buildPage() {
    // build the indicator accordion
    this.info.sections = [];
    this.info.allInfo = {};

    // build the allBox Info
    this.info.allInfo.name = "All Indicators";
    this.info.allInfo.id = "cb.-1.-1";
    this.info.allInfo.checked = false;

    for (let i = 0; i < customTables.length; i += 1) {
      const indicatorSection = customTables[i];
      const sectionInfo = {};
      sectionInfo.indicators = [];

      // build a sectionBox Info
      sectionInfo.name = indicatorSection.SectionName;
      sectionInfo.id = `cb.${i}.-1`;
      sectionInfo.checked = false;

      for (let j = 0; j < indicatorSection.Tables.length; j += 1) {
        const indicator = indicatorSection.Tables[j];

        // build a indicatorBox Info
        const indicatorInfo = {};
        indicatorInfo.name = indicator.TableName;
        indicatorInfo.id = `cb.${i}.${j}`;
        indicatorInfo.checked = false;
        sectionInfo.indicators.push(indicatorInfo);
      }

      this.info.sections.push(sectionInfo);

      // build this sectionBox
      this.sectionAccordions.push(
        <SectionAccordion
          sectionInfo={this.info.sections[i]}
          onCheckBoxClicked={this.onCheckBoxClicked}
        />,
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
