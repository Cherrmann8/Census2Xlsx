import React from "react";
import PropTypes from "prop-types";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";

class LocationLevelButtons extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      dropDownValue: "State",
    };

    this.changeValue = this.changeValue.bind(this);
  }

  changeValue(text) {
    const { onLevelChange } = this.props;
    onLevelChange(text);
    this.setState({ dropDownValue: text });
  }

  render() {
    const { dropDownValue } = this.state;

    return (
      <div className="LocationLevelButtons">
        <span id="LocationLevelSpan">Select location level:</span>
        <DropdownButton title={dropDownValue}>
          <Dropdown.Item onClick={() => this.changeValue("State")}>
            State
          </Dropdown.Item>
          <Dropdown.Item onClick={() => this.changeValue("County")}>
            County
          </Dropdown.Item>
          <Dropdown.Item onClick={() => this.changeValue("Place")}>
            Place
          </Dropdown.Item>
        </DropdownButton>
      </div>
    );
  }
}

LocationLevelButtons.propTypes = {
  onLevelChange: PropTypes.func,
};
LocationLevelButtons.defaultProps = {
  onLevelChange: null,
};

export default LocationLevelButtons;
