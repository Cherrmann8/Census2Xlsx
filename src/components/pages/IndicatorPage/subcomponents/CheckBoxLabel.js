import React from "react";
import PropTypes from "prop-types";
import "../../../css/IndicatorPage.css";

class CheckBoxLabel extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    const { id, name, checked, onClick } = this.props;

    return (
      <>
        <label htmlFor={id}>
          <input
            type="checkbox"
            name={name}
            id={id}
            checked={checked}
            onChange={(e) => onClick(e)}
          />
          {name}
        </label>
        <br />
      </>
    );
  }
}

CheckBoxLabel.propTypes = {
  id: PropTypes.string,
  name: PropTypes.string,
  checked: PropTypes.bool,
  onClick: PropTypes.func,
};
CheckBoxLabel.defaultProps = {
  id: null,
  name: null,
  checked: false,
  onClick: null,
};

export default CheckBoxLabel;
