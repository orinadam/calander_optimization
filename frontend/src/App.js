import Navbar from "./components/Layout/Navbar"
import UploadFilesModal from "./components/UI/UploadFilesModal"
import {useState} from 'react'
import ScheduleTable from "./components/UI/Table"
import EditCandidate from "./components/UI/EditCandidate"
import {useMemo, createContext} from "react"

export const TableData = createContext({
  data: true,
  setData: () => {}
});


//until we will connect the front with the back
const staticData = [
  {"candidate" :"מועמד1", "day": "ראשון", "hour": "13:00", "psychologist": "פסיכולוג2"},
  {"candidate" :"מועמד2", "day": "שני"  , "hour": "14:00", "psychologist": "פסיכולוג3"},
  {"candidate" :"מועמד3", "day": "ראשון", "hour": "13:00", "psychologist": "פסיכולוג1"},
  {"candidate" :"מועמד4", "day": "שלישי", "hour": "12:00", "psychologist": "פסיכולוג2"},
  {"candidate" :"מועמד5", "day": "חמישי", "hour": "15:00", "psychologist": "פסיכולוג3"},
  {"candidate" :"מועמד6", "day": "ראשון", "hour": "13:00", "psychologist": "פסיכולוג1"}
]

function App() {
  //Upload Files
  const [formModal, setFormModal] = useState(false)
  const [errorModal, setErrorModal] = useState(false)

  //Schedule
  const [data, setData] = useState(staticData)


  //Edit Candidate Modal
  const [candidateModal, setCandidateModal] = useState(false)
  const [errorCandidateModal, setErrorCandidateModal] = useState(false)  
  const [candidate, setCandidate] = useState({})

  const closeModal = (errFunc, formFunc) =>
  {
    errFunc(false)
    formFunc(false)
  }
  const value = useMemo(() => ({ data, setData }), [data]);
  return (
    <TableData.Provider value={value}>
      {/*header*/}
      <Navbar  onClickForm={() => {setFormModal(true)}}/>
      {/*modals*/}
      {formModal && <UploadFilesModal  changeError={setErrorModal} showError={errorModal} show={formModal} onHide={() => {closeModal(setErrorModal,setFormModal)}} />}
      {candidateModal && <EditCandidate  changeError={setErrorCandidateModal} showError={errorCandidateModal} show={candidateModal} onHide={() => {closeModal(setErrorModal,setCandidateModal)}} />}
       {/*body*/}
      <ScheduleTable openCandidate={()=> {setCandidateModal(true)}}  data={data} editData={setData}/>
      </TableData.Provider>
  );
}

export default App;