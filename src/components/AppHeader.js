import React from "react";
import PropTypes from "prop-types";
import AppNav from "./AppNav";

class AppHeader extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    const { page } = this.props;

    return (
      <>
        <h1>Census2Xlsx</h1>
        <div className="App-nav">
          <AppNav page={page} />
        </div>
      </>
    );
  }
}

AppHeader.propTypes = {
  page: PropTypes.number,
};
AppHeader.defaultProps = {
  page: 0,
};

export default AppHeader;
