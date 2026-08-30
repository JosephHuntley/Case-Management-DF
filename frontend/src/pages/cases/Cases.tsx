import './Cases.css'
import Button from '../../components/Button/Button'
import { useState } from 'react'

function Cases() {
  const [activeFilter, setActiveFilter] = useState<string>('all')

  

  return (
    <main>
      <div id='cases-header'>
        <div id="cases-filter-btn">
          <div className={`${activeFilter == 'all' ? 'cases-active' : ''}`} onClick={() => setActiveFilter('all')}>All</div>
          <div className={`${activeFilter == 'active' ? 'cases-active' : ''}`} onClick={() => setActiveFilter('active')}>Active</div>
          <div className={`${activeFilter == 'in_review' ? 'cases-active' : ''}`} onClick={() => setActiveFilter('in_review')}>In Review</div>
          <div className={`${activeFilter == 'closed' ? 'cases-active' : ''}`} onClick={() => setActiveFilter('closed')}>Closed</div>
        </div>
        <Button id="cases-new-button" text="+ New Case"/>
      </div>
    </main>
  )
}

export default Cases