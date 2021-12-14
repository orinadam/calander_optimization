import Navbar from "./components/Layout/Navbar"
import UploadFilesModal from "./components/UI/UploadFilesModal"
import {useState} from 'react'
import ScheduleTable from "./components/UI/Table"

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
  const [formModal, setFormModal] = useState(false)
  const [errorModal, setErrorModal] = useState(false)
  const [data, setData] = useState(staticData)


  


  const closeModal = () =>
  {
    setErrorModal(false)
    setFormModal(false)
  }
  return (
    <div>
      <Navbar  onClickForm={() => {setFormModal(true)}}/>
      {formModal && <UploadFilesModal  changeError={setErrorModal} showError={errorModal} show={formModal} onHide={closeModal} />}
      <ScheduleTable data={data} editData={setData}/>
    </div>
  );
}

export default App;
