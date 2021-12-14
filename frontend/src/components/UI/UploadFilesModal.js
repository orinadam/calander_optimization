import { Button, Modal, Form, Alert} from "react-bootstrap";
import {useState} from 'react'
import axios from 'axios'

const FormModal = (props) => {
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
            <Form noValidate validated={validated} onSubmit={handleSubmit}>
                <Form.Group controlId="formFile" className="mb-3">
                    {createFormFiles}
                </Form.Group>
                <Button variant="primary" type="submit">הכן לו"ז</Button>

            </Form>
       
        </Modal.Body>
        <Modal.Footer>
          <Button onClick={props.onHide}>סגירה</Button>
        </Modal.Footer>
      </Modal>
    </div>

   
  );
};

export default FormModal;
