import React from 'react'
import PropTypes from 'prop-types'
import Accordion from 'react-bootstrap/Accordion'
import Card from 'react-bootstrap/Card'
import ListGroup from 'react-bootstrap/ListGroup'

class SelectionTable extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
    }

    this.selectionList = []

    this.buildSelectionTable = this.buildSelectionTable.bind(this)
  }

  buildSelectionTable() {
    console.log('Building selectionTable')

    const { locationList, locations } = this.props
    this.selectionList = []
    let itemID = 0

    locationList.forEach((location) => {
      if (location.stateIdx === -1) {
        console.log('Invalid location in locationList')
      } else {
        if (location.countyIdx !== -1 && location.placeIdx !== -1) {
          console.log('Invalid location in locationList')
        } else if (location.countyIdx === -1 && location.placeIdx === -1) {
          this.selectionList.push(
            <ListGroup.Item eventKey={itemID} key={itemID}>
              {locations[location.stateIdx].StateName}
            </ListGroup.Item>,
          )
        } else if (location.countyIdx !== -1) {
          this.selectionList.push(
            <ListGroup.Item eventKey={itemID} key={itemID}>
              {locations[location.stateIdx].Counties[location.countyIdx].CountyName}
            </ListGroup.Item>,
          )
        } else if (location.placeIdx !== -1) {
          this.selectionList.push(
            <ListGroup.Item eventKey={itemID} key={itemID}>
              {locations[location.stateIdx].Places[location.placeIdx].PlaceName}
            </ListGroup.Item>,
          )
        }
      }

      itemID += 1
    })
  }

  render() {
    return (
      <div id="SelectionTable">
        <Accordion defaultActiveKey="0" activeKey="0">
          <Card>
            <Card.Header>
              <h6>
                Report Area
              </h6>
            </Card.Header>
            <Accordion.Collapse eventKey="0">
              <Card.Body id="SelectionList">
                <ListGroup variant="flush">
                  {this.selectionList}
                </ListGroup>
              </Card.Body>
            </Accordion.Collapse>
          </Card>
        </Accordion>
      </div>
    )
  }
}

SelectionTable.propTypes = {
  locationList: PropTypes.arrayOf(
    PropTypes.shape({
      stateIdx: PropTypes.number,
      countyIdx: PropTypes.number,
      placeIdx: PropTypes.number,
    }),
  ),
  locations: PropTypes.arrayOf(
    PropTypes.shape({
      StateName: PropTypes.string,
      StateID: PropTypes.string,
      Counties: PropTypes.arrayOf(
        PropTypes.shape({
          CountyName: PropTypes.string,
          CountyID: PropTypes.string,
        }),
      ),
      Places: PropTypes.arrayOf(
        PropTypes.shape({
          PlaceName: PropTypes.string,
          PlaceID: PropTypes.string,
        }),
      ),
    }),
  ),
}
SelectionTable.defaultProps = {
  locationList: null,
  locations: null,
}

export default SelectionTable
