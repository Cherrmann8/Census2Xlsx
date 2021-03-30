import React from "react";
import PropTypes from "prop-types";
import ProgressBar from "react-bootstrap/ProgressBar";
import Button from "react-bootstrap/Button";
import "../../css/LoadingPage.css";

class LoadingPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  componentDidMount() {
    const { onPageMount } = this.props;
    onPageMount();
  }

  render() {
    const { progress } = this.props;

    return (
      <div className="pbar">
        <ProgressBar now={progress} label={`${progress}%`} className="pbar" />
      </div>
    );
  }
}

LoadingPage.propTypes = {
  progress: PropTypes.number,
  onPageMount: PropTypes.func,
};
LoadingPage.defaultProps = {
  progress: 0,
  onPageMount: null,
};

export default LoadingPage;
