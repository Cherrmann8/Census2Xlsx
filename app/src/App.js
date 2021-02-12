import React from 'react'
import 'bootstrap/dist/css/bootstrap.min.css'
import './App.css'
import AppHeader from './components/AppHeader'
import AppSection from './components/AppSection'
import AppFooter from './components/AppFooter'

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      page: 0,
    }

    this.handlePageChange = this.handlePageChange.bind(this)
  }

  handlePageChange(increment) {
    const { page } = this.state
    if (page + increment <= 4 && page + increment >= 0) {
      this.setState({ page: page + increment })
    } else if (page + increment === 5) {
      this.setState({ page: 0 })
    }
  }

  render() {
    const { page } = this.state

    return (
      <div className="App">
        <div className="App-header">
          <AppHeader page={page} />
        </div>

        <div className="App-section">
          <AppSection page={page} onPageChange={this.handlePageChange} />
        </div>

        <div className="App-footer">
          <AppFooter page={page} onPageChange={this.handlePageChange} />
        </div>
      </div>
    )
  }
}

export default App
