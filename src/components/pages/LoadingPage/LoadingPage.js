import React from 'react'
import PropTypes from 'prop-types'
import ProgressBar from 'react-bootstrap/ProgressBar'

const electron = window.require('electron')
const { ipcRenderer } = electron

class LoadingPage extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      progress: 0,
    }
  }

  componentDidMount() {
    ipcRenderer.send('START_BACKGROUND_VIA_MAIN', {
      number: 25,
    })

    this.timerID = setInterval(
      () => this.tick(),
      1000,
    )
  }

  componentWillUnmount() {
    clearInterval(this.timerID)
  }

  tick() {
    const { onPageChange } = this.props
    const { progress } = this.state
    this.setState({ progress: (progress + 50) })
    if (progress >= 100) {
      onPageChange(1)
    }
  }

  render() {
    const { progress } = this.state

    return (
      <div>
        <ProgressBar now={progress} label={`${progress}%`} />
      </div>
    )
  }
}

LoadingPage.propTypes = {
  onPageChange: PropTypes.func,
}
LoadingPage.defaultProps = {
  onPageChange: null,
}

export default LoadingPage
