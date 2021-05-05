import React from "react";
import "../../css/GraphPage.css";

class GraphPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <div className="GraphPage">
        <span id="OutputMessage">Your xlsx file has been successfully generated.</span>
      </div>
    );
  }
}

export default GraphPage;
