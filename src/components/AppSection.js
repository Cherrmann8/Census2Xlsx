import React from 'react'
import PropTypes from 'prop-types'
import LocationPage from './pages/LocationPage/LocationPage'
import IndicatorPage from './pages/IndicatorPage/IndicatorPage'
import ConfirmationPage from './pages/ConfirmationPage/ConfirmationPage'
import LoadingPage from './pages/LoadingPage/LoadingPage'
import GraphPage from './pages/GraphPage/GraphPage'

const electron = window.require('electron')
const { ipcRenderer } = electron

class AppSection extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      locationList: [],
      indicatorList: [],
    }

    this.addLocation = this.addLocation.bind(this)
    this.removeLocation = this.removeLocation.bind(this)
    this.addIndicator = this.addIndicator.bind(this)
    this.removeIndicator = this.removeIndicator.bind(this)

    ipcRenderer.on('MESSAGE_FROM_BACKGROUND_VIA_MAIN', (event, args) => {
      console.log(args)
    })
    ipcRenderer.on('report', (event, args) => {
      console.log(args)
    })
  }

  addLocation(stateIdx, countyIdx, placeIdx) {
    const { locationList } = this.state
    const idx = locationList.findIndex(
      (i) => (i.stateIdx === stateIdx
        && i.countyIdx === countyIdx
        && i.placeIdx === placeIdx),
    )
    if (idx === -1) {
      locationList.push({ stateIdx, countyIdx, placeIdx })
      this.setState({ locationList })
    }
  }

  removeLocation(locationIdx) {
    const { locationList } = this.state

    if (locationList.length > locationIdx) {
      locationList.splice(locationIdx, 1)
      this.setState({ locationList })
    }
  }

  addIndicator(indicatorIdx, sectionIdx, tableIdx) {
    const { indicatorList } = this.state
    indicatorList.push({ indicatorIdx, sectionIdx, tableIdx })
    this.setState({ indicatorList })
    console.log(indicatorList)
  }

  removeIndicator(indicatorIdx, sectionIdx, tableIdx) {
    const { indicatorList } = this.state
    const idx = indicatorList.findIndex(
      (i) => (i.indicatorIdx === indicatorIdx
        && i.sectionIdx === sectionIdx
        && i.tableIdx === tableIdx),
    )
    if (idx !== -1) {
      indicatorList.splice(idx, 1)
      this.setState({ indicatorList })
    }

    console.log(indicatorList)
  }

  render() {
    const { page, onPageChange } = this.props
    const { locationList, indicatorList } = this.state

    let section
    if (page === 0) {
      section = (
        <LocationPage
          locationList={locationList}
          onAddLocation={this.addLocation}
          onRemoveLocation={this.removeLocation}
        />
      )
    } else if (page === 1) {
      section = (
        <IndicatorPage
          indicatorList={indicatorList}
          onAddIndicator={this.addIndicator}
          onRemoveIndicator={this.removeIndicator}
        />
      )
    } else if (page === 2) {
      section = (
        <ConfirmationPage
          locationList={locationList}
          indicatorList={indicatorList}
        />
      )
    } else if (page === 3) {
      section = <LoadingPage onPageChange={onPageChange} />
    } else if (page === 4) {
      section = <GraphPage />
    }
    return (
      <>
        {section}
      </>
    )
  }
}

AppSection.propTypes = {
  page: PropTypes.number,
  onPageChange: PropTypes.func,
}
AppSection.defaultProps = {
  page: 0,
  onPageChange: null,
}

export default AppSection
