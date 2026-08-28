import { useParams } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext'
import './Evidence.css'
import EvidenceSearch from './EvidenceSearh'
import EvidenceDetail from './EvidenceDetail'

interface EvidenceParams{
  evidenceId?: string
  [key: string]: string | undefined
}



function Evidence() {
  const {evidenceId} = useParams<EvidenceParams>();
  return(
  <>
  {
    evidenceId ? 
    <EvidenceDetail/>: 
    <EvidenceSearch/> 
  }
    

  </>
    )
}

export default Evidence