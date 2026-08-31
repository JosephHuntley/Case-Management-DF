import './Cases.css'
import Button from '../../components/Button/Button'
import { useState, useEffect } from 'react'
import {useAuth} from '../../context/AuthContext'
import type {Case} from '../../types'
import { formatTimestamp } from "../chainOfCustody/utils";
import {CaseStatusLabels} from '../../types'
import CreateCase from '../../components/CreateCase/CreateCase'

function Cases() {
  const [activeFilter, setActiveFilter] = useState<string>('all')
  const [cases, setCases] = useState<Case[]>([])
  const [casesFiltered, setCasesFiltered] = useState<Case[]>([])
  const [isOpen, setIsOpen] = useState<boolean>(false)
  
  const { getAccessToken } = useAuth(); 

  useEffect(() => {

    const fetchCases = async () => {

         try {
          const token = await getAccessToken();
          const res = await fetch('/api/cases/', {
            headers: token ? { Authorization: `Bearer ${token}` } : {},
            credentials: 'include',
          })
          if (!res.ok) {
            throw new Error(`Error fetching cases: ${res.statusText}`)
          }
          
          const data: Case[] = await res.json()
          setCases(data)
          setCasesFiltered(data)
          console.log(data)
        }catch (error){
          console.error(error)
        }
    }

    fetchCases()

  }, [])

  useEffect(() => {
    if (activeFilter == 'all'){
      setCasesFiltered(cases)
    }else{
      const temp = cases.filter(c => c.status == activeFilter);
      setCasesFiltered(temp);
    }
  }, [activeFilter])

  return (
    <main id="cases-page">
      <div id='cases-header'>
        <div id="cases-filter-btn">
          <div className={`${activeFilter == 'all' ? 'cases-active' : ''}`} onClick={() => setActiveFilter('all')}>All</div>
          <div className={`${activeFilter == 'open' ? 'cases-active' : ''}`} onClick={() => setActiveFilter('open')}>Active</div>
          <div className={`${activeFilter == 'in progress' ? 'cases-active' : ''}`} onClick={() => setActiveFilter('in progress')}>In Progress</div>
          <div className={`${activeFilter == 'pending' ? 'cases-active' : ''}`} onClick={() => setActiveFilter('pending')}>In Review</div>
          <div className={`${activeFilter == 'closed' ? 'cases-active' : ''}`} onClick={() => setActiveFilter('closed')}>Closed</div>
        </div>
        <Button onClick={() => setIsOpen(true)} id="cases-new-button" text="+ New Case" />
      </div>
      <div className='card'>
        <table id='cases-table'>
          <thead>
            <tr>
             <th>Case #</th>
             <th>Title</th>
             <th>Status</th>
             <th>Investigator</th>
             <th>Opened</th>
             <th>Evidence</th>
            </tr>
          </thead>
          <tbody>
            {casesFiltered.map((c, i) => (
              <tr key={c.id} className={`${i == casesFiltered.length - 1 ? 'no-border' : ''}`}>
                <td className='cases-case-title'>
                  {c.case_number}
                </td>
                <td>
                  {c.title}
                </td>
                <td >
                  <span 
                  className={`badge ${c.status == "open" || c.status == 'closed' ? CaseStatusLabels[c.status].toLowerCase() : 'pending'}`}>
                    {CaseStatusLabels[c.status]}
                  </span>
                </td>
                <td >
                  {
                    !c.assigned_to
                      ? "To Be Assigned"
                      : c.assigned_to.first_name && c.assigned_to.last_name
                        ? `${c.assigned_to.first_name} ${c.assigned_to.last_name}`
                        : "No user found"
                  }
                </td>
                <td className='cases-case-date'>
                  {formatTimestamp(c.created_at)}
                </td>
                <td>
                  {c.evidence.length || '0'}
                </td>

              </tr>
          ))}
          </tbody>
        </table>
      </div>
      <CreateCase isOpen={isOpen} onClose={() => setIsOpen(false)}/>
      
    </main>
  )
}

export default Cases