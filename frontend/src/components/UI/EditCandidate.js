import { Button, Modal, Form, Alert} from "react-bootstrap";
import {useState, useContext} from 'react'
import { CandidateData } from "../../App";

const StaticData = [
    {"day": "שני", "hour": "11:00", "psychologist": "פסיכולוג4"},
    {"day": "ראשון", "hour": "18:00", "psychologist": "פסיכולוג1"},
    {"day": "שישי", "hour": "08:00", "psychologist": "פסיכולוג3"},
]

const EditCandidate = (props) => {

    const {candidate, setCandidate} = useContext(CandidateData)
    const current = {"day" : candidate.day, "hour" : candidate.hour, "psychologist" : candidate.psychologist}
    const [selected, setSelected] = useState(`${current.psychologist}-${current.day}-${current.hour}`)

    const [options, setOptions] = useState(StaticData)

    const showOptions = options.map(option => {
       return  <option value={`${option.psychologist}-${option.day}-${option.hour}`}>{`${option.psychologist} - ${option.day} - ${option.hour}`}</option>

    })
    const handleSubmitUpdate = (event) => {
        event.preventDefault();
        var foundIndex = props.data.findIndex(item => item.id === candidate.id);
        const newData = props.data
        const arr = selected.split('-')
        newData[foundIndex].psychologist = arr[0]
        newData[foundIndex].day = arr[1]
        newData[foundIndex].hour = arr[2]
        props.editdata(newData)
        props.onHide()
        


      };
    const handleDelete = (item) =>
    {
        const newData = props.data.filter(obj => {
            return obj.id !== item.id
        })
        props.editdata(newData)
        props.onHide()
    }
  return (
    <div>
      <Modal 
        {...props}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter "
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">
            :בניית לו"ז
          </Modal.Title>
        </Modal.Header>
        {(props.showerror === 1) && <Alert variant={'danger'}>הפעולה נכשלה</Alert>}
        <Modal.Body>
        <Form onSubmit={handleSubmitUpdate}>
        <Form.Select onChange={(e) => setSelected(e.target.value)}aria-label="Default select example">
        <Form.Text>Text</Form.Text>
        {/*the current sitution*/}
        <option value={`${current.psychologist}-${current.day}-${current.hour}`}>{`${current.psychologist} - ${current.day} - ${current.hour}`}</option>
        {showOptions}
        </Form.Select>
        <br />
        <div>
            <Button variant="success" type="submit">עדכן</Button>{' '}
            <Button onClick={() => {handleDelete(candidate)}} variant="danger" type="submit">מחק</Button>
        </div>
        </Form>       
        </Modal.Body>
        <Modal.Footer>
          <Button onClick={props.onHide}>סגירה</Button>
        </Modal.Footer>
      </Modal>
    </div>

   
  );
};

export default EditCandidate;
