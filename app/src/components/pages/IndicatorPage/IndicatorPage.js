import React from 'react'
import PropTypes from 'prop-types'
import Button from 'react-bootstrap/Button'
import Accordion from 'react-bootstrap/Accordion'
import Card from 'react-bootstrap/Card'
import dataTables from '../../../assets/data/dataTableDescriptions.json'
import '../../css/IndicatorPage.css'

class IndicatorPage extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
    }

    this.indicatorSections = []
    this.sectionCheckBoxes = {}
    this.checkBoxInfo = []

    this.onCheckBoxClicked = this.onCheckBoxClicked.bind(this)

    // build the indicatorAccordion
    this.buildIndicatorAccordion()
  }

  componentDidMount() {
    const { indicatorList } = this.props
    indicatorList.forEach((indicator) => {
      const index = indicator.indicatorIdx.toString()
      document.getElementById(index).checked = true
      this.checkBoxInfo[index].checked = true
    })
  }

  onCheckBoxClicked(event) {
    const id = parseInt(event.target.id, 10)
    const { sid, tid } = this.checkBoxInfo[id]
    const { onAddIndicator, onRemoveIndicator } = this.props

    this.checkBoxInfo[id].checked = !this.checkBoxInfo[id].checked
    document.getElementById(event.target.id).checked = this.checkBoxInfo[id].checked

    // console.log(`${id}, ${sid}, ${tid}`)

    if (this.checkBoxInfo[id].checked) {
      // console.log('add')
      onAddIndicator(id, sid, tid)
    } else {
      // console.log('remove')
      onRemoveIndicator(id, sid, tid)
    }
  }

  buildIndicatorAccordion() {
    // build the indicator accordion
    let i
    let j
    let checkboxID = 0

    for (i = 0; i < dataTables.length; i += 1) {
      const indicatorSection = dataTables[i]
      this.sectionCheckBoxes[i] = []

      // build this sections checkboxes
      for (j = 0; j < indicatorSection.Indicators.length; j += 1) {
        const indicator = indicatorSection.Indicators[j]

        let cbInfo = {}
        cbInfo.name = indicator.TableName
        cbInfo.id = checkboxID.toString()
        cbInfo.sid = i
        cbInfo.tid = j
        cbInfo.checked = false
        this.checkBoxInfo.push(cbInfo)

        this.sectionCheckBoxes[i].push(
          <div>
            <input
              type="checkbox"
              name={this.checkBoxInfo[checkboxID].name}
              id={this.checkBoxInfo[checkboxID].id}
              onChange={(e) => this.onCheckBoxClicked(e)}
            />
            <label htmlFor={this.checkBoxInfo[checkboxID].id}>
              {this.checkBoxInfo[checkboxID].name}
            </label>
            <br />
          </div>,
        )

        checkboxID += 1
      }

      // build this sections accordion
      this.indicatorSections.push(
        <Accordion defaultActiveKey="0">
          <Card>
            <Card.Header id="indicatorHeader">
              <Accordion.Toggle as={Card.Header} variant="link" eventKey="0">
                {indicatorSection.IndicatorSectionName}
              </Accordion.Toggle>
            </Card.Header>
            <Accordion.Collapse eventKey="0">
              <Card.Body>
                {this.sectionCheckBoxes[i]}
              </Card.Body>
            </Accordion.Collapse>
          </Card>
        </Accordion>,
      )
    }
  }

  render() {
    return (
      <div id="IndicatorAccordion">
        {this.indicatorSections}
      </div>
    )
  }
}

IndicatorPage.propTypes = {
  indicatorList: PropTypes.arrayOf(
    PropTypes.shape({
      indicatorIdx: PropTypes.number,
      sectionIdx: PropTypes.number,
      tableIdx: PropTypes.number,
    }),
  ),
  onAddIndicator: PropTypes.func,
  onRemoveIndicator: PropTypes.func,
}
IndicatorPage.defaultProps = {
  indicatorList: null,
  onAddIndicator: null,
  onRemoveIndicator: null,
}

export default IndicatorPage
