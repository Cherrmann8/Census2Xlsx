import React from "react";
import PropTypes from "prop-types";
import Button from "react-bootstrap/Button";
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
    onPageChange(1);
  }

  lastPageClick() {
    const { onPageChange } = this.props;
    onPageChange(-1);
  }

  render() {
    const { page } = this.props;

    let b1 = null;
    let b2 = null;
    if (page === 1 || page === 2) {
      b1 = (
        <Button variant="primary" onClick={this.lastPageClick}>
          Back
        </Button>
      );
    }

    if (page === 0 || page === 1) {
      b2 = (
        <Button variant="primary" onClick={this.nextPageClick}>
          Next
        </Button>
      );
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
};
AppFooter.defaultProps = {
  page: 0,
  onPageChange: null,
};

export default AppFooter;
