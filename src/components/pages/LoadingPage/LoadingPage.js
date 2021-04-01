import React from "react";
import PropTypes from "prop-types";
import ProgressBar from "react-bootstrap/ProgressBar";
import Button from "react-bootstrap/Button";
import "../../css/LoadingPage.css";

const electron = window.require("electron");
const { ipcRenderer } = electron;

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
    const { progress, progressDialog } = this.props;

    return (
      <div className="ProgressInfo">
        <ProgressBar now={progress} label={`${progress}%`} id="ProgressBar" />
        <span id="ProgressDialog">{progressDialog}</span>
      </div>
    );
  }
}

LoadingPage.propTypes = {
  progress: PropTypes.number,
  progressDialog: PropTypes.string,
  onPageMount: PropTypes.func,
};
LoadingPage.defaultProps = {
  progress: 0,
  progressDialog: "",
  onPageMount: null,
};

export default LoadingPage;
