import React from "react";
import PropTypes from "prop-types";
import "./css/AppNav.css";

function AppNav(props) {
  const { page } = props;
  let title;

  if (page === 0) {
    title = "Select Report Area";
  } else if (page === 1) {
    title = "Select Report Tables";
  } else if (page === 2) {
    title = "Confirm Report";
  } else if (page === 4) {
    title = "Finished";
  }

  return (
    <div id="AppNav">
      <div id="AppNavHeader">
        <h4 id="NavPage">
          {title}
        </h4>
      </div>
    </div>
  );
}

AppNav.propTypes = {
  page: PropTypes.number,
};
AppNav.defaultProps = {
  page: 0,
};

export default AppNav;
