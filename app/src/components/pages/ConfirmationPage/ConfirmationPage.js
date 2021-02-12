import React from 'react'
import PropTypes from 'prop-types'
import ListGroup from 'react-bootstrap/ListGroup'

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
      this.lList.push(
        <ListGroup.Item
          action
          eventKey={itemID}
          key={itemID}
        >
          {location.stateIdx}
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
          {indicator.indicatorIdx}
        </ListGroup.Item>,
      )
      itemID += 1
    })

    return (
      <div>
        <span>Confirmation Page stuff</span>
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
