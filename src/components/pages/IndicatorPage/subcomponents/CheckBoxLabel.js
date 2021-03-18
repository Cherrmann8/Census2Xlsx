import React from "react";
import PropTypes from "prop-types";
import "../../../css/IndicatorPage.css";

class CheckBoxLabel extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    const { info, onCheckBoxClicked } = this.props

    return (
      <>
        <label htmlFor={info.id}>
          <input
            type="checkbox"
            name={info.name}
            id={info.id}
            onChange={(e) => onCheckBoxClicked(e)}
          />
          {info.name}
        </label>
        <br />
      </>
    );
  }
}

CheckBoxLabel.propTypes = {
  info: PropTypes.shape({
    name: PropTypes.string,
    id: PropTypes.string,
    sid: PropTypes.number,
    tid: PropTypes.number,
  }),
  onCheckBoxClicked: PropTypes.func,
};
CheckBoxLabel.defaultProps = {
  info: null,
  onCheckBoxClicked: null,
};

export default CheckBoxLabel;
