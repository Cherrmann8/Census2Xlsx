import React from 'react'
import PropTypes from 'prop-types'
import ListGroup from 'react-bootstrap/ListGroup'
import locations from '../../../assets/data/geographies.json'
import dataTables from '../../../assets/data/dataTableDescriptions.json'

class ConfirmationPage extends React.Component {
  constructor(props) {
    super(props)
    this.state = {}

    this.lList = []
    this.iList = []
  }

  render() {
    const { locationList, indicatorList } = this.props

    let itemID = 0
    locationList.forEach((location) => {
      let locationName
      if (location.countyIdx === -1 && location.placeIdx === -1) {
        locationName = locations[location.stateIdx].StateName
      } else if (location.countyIdx !== -1 && location.placeIdx === -1) {
        locationName = locations[location.stateIdx].Counties[location.countyIdx].CountyName
      } else if (location.countyIdx === -1 && location.placeIdx !== -1) {
        locationName = locations[location.stateIdx].Places[location.placeIdx].PlaceName
      }

      this.lList.push(
        <ListGroup.Item
          action
          eventKey={itemID}
          key={itemID}
        >
          {locationName}
        </ListGroup.Item>,
      )
      itemID += 1
    })

    itemID = 0
    indicatorList.forEach((indicator) => {
      this.iList.push(
        <ListGroup.Item
          action
          eventKey={itemID}
          key={itemID}
        >
          {dataTables[indicator.sectionIdx].Indicators[indicator.tableIdx].TableName}
        </ListGroup.Item>,
      )
      itemID += 1
    })

    return (
      <div>
        <ListGroup>
          {this.lList}
        </ListGroup>
        <ListGroup>
          {this.iList}
        </ListGroup>
      </div>
    )
  }
}

ConfirmationPage.propTypes = {
  locationList: PropTypes.arrayOf(
    PropTypes.shape({
      stateIdx: PropTypes.number,
      countyIdx: PropTypes.number,
      placeIdx: PropTypes.number,
    }),
  ),
  indicatorList: PropTypes.arrayOf(
    PropTypes.shape({
      indicatorIdx: PropTypes.number,
      sectionIdx: PropTypes.number,
      tableIdx: PropTypes.number,
    }),
  ),
}
ConfirmationPage.defaultProps = {
  locationList: null,
  indicatorList: null,
}

export default ConfirmationPage
