import React from "react";
import PropTypes from "prop-types";
import Button from "react-bootstrap/Button";
import Tooltip from "react-bootstrap/Tooltip";
import OverlayTrigger from "react-bootstrap/OverlayTrigger";
import "./css/AppFooter.css";

class AppFooter extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};

    this.nextPageClick = this.nextPageClick.bind(this);
    this.lastPageClick = this.lastPageClick.bind(this);
  }

  nextPageClick() {
    const { onPageChange } = this.props;
    onPageChange(1, true);
  }

  lastPageClick() {
    const { onPageChange } = this.props;
    onPageChange(-1, true);
  }

  render() {
    const { page, invalidLocations, invalidIndicators } = this.props;

    let b1 = null;
    let b2 = null;
    if (page === 1 || page === 2) {
      b1 = (
        <Button variant="primary" onClick={this.lastPageClick}>
          Back
        </Button>
      );
    }

    if (page === 0) {
      if (invalidLocations) {
        b2 = (
          <OverlayTrigger
            placement="left"
            className="ErrorMessage"
            overlay={(
              <Tooltip>
                At least one location required
              </Tooltip>
            )}
          >
            <span className="d-inline-block">
              <Button variant="primary" disabled={invalidLocations} style={{ pointerEvents: "none" }} onClick={this.nextPageClick}>
                Next
              </Button>
            </span>
          </OverlayTrigger>
        );
      } else {
        b2 = (
          <Button variant="primary" onClick={this.nextPageClick}>
            Next
          </Button>
        );
      }
    } else if (page === 1) {
      if (invalidIndicators) {
        b2 = (
          <OverlayTrigger
            placement="left"
            className="ErrorMessage"
            overlay={(
              <Tooltip>
                At least one Indicator required
              </Tooltip>
            )}
          >
            <span className="d-inline-block">
              <Button variant="primary" disabled={invalidIndicators} style={{ pointerEvents: "none" }} onClick={this.nextPageClick}>
                Next
              </Button>
            </span>
          </OverlayTrigger>
        );
      } else {
        b2 = (
          <Button variant="primary" onClick={this.nextPageClick}>
            Next
          </Button>
        );
      }
    } else if (page === 2) {
      b2 = (
        <Button variant="primary" onClick={this.nextPageClick}>
          Download
        </Button>
      );
    } else if (page === 4) {
      b2 = (
        <Button variant="primary" onClick={this.nextPageClick}>
          Start Over
        </Button>
      );
    }

    return (
      <div className="pageButtons">
        {b2}
        {b1}
      </div>
    );
  }
}

AppFooter.propTypes = {
  page: PropTypes.number,
  onPageChange: PropTypes.func,
  invalidLocations: PropTypes.bool,
  invalidIndicators: PropTypes.bool,
};
AppFooter.defaultProps = {
  page: 0,
  onPageChange: null,
  invalidLocations: true,
  invalidIndicators: true,
};

export default AppFooter;
