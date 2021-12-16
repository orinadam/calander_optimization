import { Button, Modal, Form, Alert} from "react-bootstrap";
import {useState} from 'react'
import axios from 'axios'
import { SpinnerInfinity } from "spinners-react";


const FormModal = (props) => {
    const [validated, setValidated] = useState(false);
    const [isLoading, setIsloading] = useState(false);


    const handleSubmit = (event) => {
        const form = event.currentTarget;
        if (form.checkValidity() === false) {
          event.preventDefault();
          event.stopPropagation();
          setValidated(true);

        }
        else
        {
          setIsloading(true);
        }
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
        {(props.showerror === true) ? <Alert variant={'danger'}>הפעולה נכשלה</Alert> : undefined}
        <Modal.Body>
            <Form noValidate validated={validated} onSubmit={handleSubmit}>
                <Form.Group controlId="formFile" className="mb-3">
                    {createFormFiles}
                </Form.Group>
                {!isLoading ? <Button variant="primary" type="submit">הכן לו"ז</Button> :
                <SpinnerInfinity
                size={50}
                thickness={100}
                speed={100}
                color="rgba(57, 77, 172, 1)"
                secondaryColor="rgba(0, 0, 0, 0.44)"
              />}

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
