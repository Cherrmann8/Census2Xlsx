import React from 'react'
import PropTypes from 'prop-types'
import ProgressBar from 'react-bootstrap/ProgressBar'

class LoadingPage extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      progress: 0,
    }
  }

  componentDidMount() {
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
    this.setState({ progress: (progress + 20) })
    if (progress >= 100) {
      onPageChange(1)
    }
  }

  render() {
    const { progress } = this.state

    return (
      <div>
        <span>Loading Page stuff</span>
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
