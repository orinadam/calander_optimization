import { Button, Modal, Form, Alert} from "react-bootstrap";
import {useState} from 'react'
import axios from 'axios'

const EditCandidate = (props) => {
    const [validated, setValidated] = useState(false);

    const handleSubmit = (event) => {
        const form = event.currentTarget;
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
        }
    
        setValidated(true);
      };
    const formLabels = ["מועמדים", "פסיכולוגים", "זמני פסיכולוגים", "התניות", "התניות על מועמדים","זמני מועמדים"]
    const createFormFiles = formLabels.map(label =>
        {
            return(
            <>
                <Form.Label>{`:${label}`}</Form.Label>
                <Form.Control required type="file" />
            </>
    )})

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
        {props.showError && <Alert variant={'danger'}>הפעולה נכשלה</Alert>}
        <Modal.Body>
        <Form>
        <Form.Select aria-label="Default select example">
        <Form.Text>Text</Form.Text>
        <option>Open this select menu</option>
        <option value="1">One</option>
        <option value="2">Two</option>
        <option value="3">Three</option>
        </Form.Select>


        <Button variant="primary" type="submit">עדכן</Button>
        <Button variant="primary" type="submit">מחק</Button>
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
