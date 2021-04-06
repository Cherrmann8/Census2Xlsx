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
        <span id="OutputMessage">Finished!</span>
      </div>
    );
  }
}

export default GraphPage;
