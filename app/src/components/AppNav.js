import React from 'react'
import PropTypes from 'prop-types'

function AppNav(props) {
  const { page } = props
  let title
  if (page === 0) {
    title = <span>Location Page</span>
  } else if (page === 1) {
    title = <span>Indicator Page</span>
  } else if (page === 2) {
    title = <span>Confirmation Page</span>
  } else if (page === 3) {
    title = <span>Loading Page</span>
  } else if (page === 4) {
    title = <span>Graph Page</span>
  }

  return (
    <div>
      {title}
    </div>
  )
}

AppNav.propTypes = {
  page: PropTypes.number,
}
AppNav.defaultProps = {
  page: 0,
}

export default AppNav
