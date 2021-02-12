import React from 'react'
import PropTypes from 'prop-types'
import Button from 'react-bootstrap/Button'
import LocationLevelButtons from './subcomponents/LocationLevelButtons'
import SelectorTable from './subcomponents/SelectorTable'
import SelectionTable from './subcomponents/SelectionTable'
import locations from '../../../assets/data/geographies.json'
import '../../css/LocationPage.css'

class LocationPage extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      level: 'State',
      activeCard: '0',
      stateListTitle: 'Select a state:',
      stateIdx: -1,
      countyIdx: -1,
      placeIdx: -1,
    }

    this.selectionTable = React.createRef()

    this.handleLevelChange = this.handleLevelChange.bind(this)
    this.handleOpenSecondary = this.handleOpenSecondary.bind(this)
    this.handleAddClick = this.handleAddClick.bind(this)
    this.setStateIdx = this.setStateIdx.bind(this)
    this.setCountyIdx = this.setCountyIdx.bind(this)
    this.setPlaceIdx = this.setPlaceIdx.bind(this)
  }

  componentDidMount() {
    // rebuild the selectionList in SelectionTable when this page is mounted
    this.selectionTable.current.buildSelectionTable()
    this.selectionTable.current.forceUpdate()
  }

  handleLevelChange(newLevel) {
    this.setState({
      level: newLevel,
      activeCard: '0',
      stateListTitle: 'Select a state:',
      stateIdx: -1,
      countyIdx: -1,
      placeIdx: -1,
    })
  }

  handleOpenSecondary(stateName) {
    this.setState({ activeCard: '1', stateListTitle: `State selected: ${stateName}` })
  }

  handleAddClick() {
    const { onAddLocation } = this.props
    const {
      stateIdx,
      countyIdx,
      placeIdx,
    } = this.state

    if (stateIdx !== -1) {
      onAddLocation(stateIdx, countyIdx, placeIdx)
      this.selectionTable.current.buildSelectionTable()
    }
  }

  setStateIdx(newIdx) {
    this.setState({ stateIdx: newIdx })
  }

  setCountyIdx(newIdx) {
    this.setState({ countyIdx: newIdx })
  }

  setPlaceIdx(newIdx) {
    this.setState({ placeIdx: newIdx })
  }

  render() {
    const { locationList } = this.props
    const {
      level,
      activeCard,
      stateListTitle,
    } = this.state

    return (
      <div className="LocationPage">
        <LocationLevelButtons onLevelChange={this.handleLevelChange} />
        <div className="LocationTables">
          <SelectorTable
            level={level}
            activeCard={activeCard}
            stateListTitle={stateListTitle}
            onOpenSecondary={this.handleOpenSecondary}
            setStateIdx={this.setStateIdx}
            setCountyIdx={this.setCountyIdx}
            setPlaceIdx={this.setPlaceIdx}
            locations={locations}
          />
          <div className="LocationTableButtons">
            <Button onClick={this.handleAddClick}>Add</Button>
            <Button>Remove</Button>
          </div>
          <SelectionTable
            ref={this.selectionTable}
            locationList={locationList}
            locations={locations}
          />
        </div>
      </div>
    )
  }
}

LocationPage.propTypes = {
  locationList: PropTypes.arrayOf(
    PropTypes.shape({
      stateIdx: PropTypes.number,
      countyIdx: PropTypes.number,
      placeIdx: PropTypes.number,
    }),
  ),
  onAddLocation: PropTypes.func,
}
LocationPage.defaultProps = {
  locationList: null,
  onAddLocation: null,
}

export default LocationPage
