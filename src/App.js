import React from "react";
import AppHeader from "./components/AppHeader";
import AppSection from "./components/AppSection";
import AppFooter from "./components/AppFooter";
import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      page: 0,
      invalidLocations: true,
      invalidIndicators: true,
    };

    this.appSection = React.createRef();

    this.handlePageChange = this.handlePageChange.bind(this);
    this.setInvalidLocations = this.setInvalidLocations.bind(this);
    this.setInvalidIndicators = this.setInvalidIndicators.bind(this);
    this.incPage = this.incPage.bind(this);
    this.decPage = this.decPage.bind(this);
  }

  componentDidMount() {
    const navPage = document.getElementById("NavPage");
    navPage.addEventListener("animationend", (e) => {
      if (navPage.className === "exitRight") {
        navPage.className = "enterLeft";
        this.decPage();
      } else if (navPage.className === "exitLeft") {
        navPage.className = "enterRight";
        this.incPage();
      } else if (navPage.className === "enterRight") {
        navPage.className += "";
      } else if (navPage.className === "enterLeft") {
        navPage.className += "";
      }
    });

    const appSection = document.getElementById("AppSection");
    appSection.addEventListener("animationend", (e) => {
      if (appSection.className === "exitRight") {
        appSection.className = "enterLeft";
      } else if (appSection.className === "exitLeft") {
        appSection.className = "enterRight";
      } else if (appSection.className === "enterRight") {
        appSection.className += "";
      } else if (appSection.className === "enterLeft") {
        appSection.className += "";
      }
    });
  }

  handlePageChange(increment) {
    const { page } = this.state;

    if (page + increment === 3) {
      if (!this.appSection.current.confirmDownload()) {
        return;
      }
    }

    const navPage = document.getElementById("NavPage");
    const appSection = document.getElementById("AppSection");

    if (increment > 0) {
      navPage.className = "exitLeft";
      appSection.className = "exitLeft";
    } else if (increment < 0) {
      navPage.className = "exitRight";
      appSection.className = "exitRight";
    }
  }

  setInvalidLocations(invalid) {
    this.setState({ invalidLocations: invalid });
  }

  setInvalidIndicators(invalid) {
    this.setState({ invalidIndicators: invalid });
  }

  incPage() {
    console.log("inc")
    const { page } = this.state;

    if (page + 1 === 5) {
      this.appSection.current.reset();
      this.setState({ page: 0 });
    } else {
      this.setState({ page: page + 1 });
    }
  }

  decPage() {
    console.log("dec")
    const { page } = this.state;

    if (page - 1 === -1) {
      this.setState({ page: 0 });
    } else {
      this.setState({ page: page - 1 });
    }
  }

  render() {
    const { page, invalidLocations, invalidIndicators } = this.state;

    return (
      <div className="App">
        <div className="App-header">
          <AppHeader page={page} />
        </div>

        <div className="App-section">
          <AppSection
            ref={this.appSection}
            page={page}
            onPageChange={this.handlePageChange}
            invalidLocations={invalidLocations}
            setInvalidLocations={this.setInvalidLocations}
            invalidIndicators={invalidIndicators}
            setInvalidIndicators={this.setInvalidIndicators}
          />
        </div>

        <div className="App-footer">
          <AppFooter
            page={page}
            onPageChange={this.handlePageChange}
            invalidLocations={invalidLocations}
            invalidIndicators={invalidIndicators}
          />
        </div>
      </div>
    );
  }
}

export default App;
