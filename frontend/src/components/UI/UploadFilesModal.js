import { Button, Modal, Form, Alert } from "react-bootstrap";
import { useState } from "react";
import axios from "axios";
import { SpinnerInfinity } from "spinners-react";

let ret = "";

const FormModal = (props) => {
  const [validated, setValidated] = useState(false);
  const [isLoading, setIsloading] = useState(false);
  const [files, setFiles] = useState([]);

  const handleChangeFile = async (e) => {
    const file = e.target.files[0];
    let data = files;
    data.push(file);
    setFiles(data);
  };
  const handleSubmit = async (event) => {
    const form = event.currentTarget;
    event.preventDefault();
    if (form.checkValidity() === false) {
      event.preventDefault();
      event.stopPropagation();
      setValidated(true);
    } else {
      setIsloading(true);
      var filenames = [
        "candidates",
        "psychologists",
        "working_hours",
        "conditions",
        "candidates_conditions",
        "candidates_available_hours",
      ];
      let final_files = files;
      const data = new FormData();
      for (var i = 0; i < filenames.length; i++) {
        data.append(filenames[i], final_files[i]);
      }
      fetch("http://127.0.0.1:5000/", {
        method: "POST",
        body: data,
      })
        .then(async (res) => {
          let data = await res.json();
          data = data["data"].filter((item, i) => {
            return i !== 0;
          });
          const final = data.map((item, i) => {
            let ret = {
              candidate: item[0],
              day: "ראשון",
              hour: item[1],
              psychologist: item[2],
              id: i,
            };
            return ret;
          });
          props.editdata(final);
          console.log(final);
        })
        .catch((err) => {
          console.log(err);
        });
    }
  };

  const formLabels = [
    "מועמדים",
    "פסיכולוגים",
    "זמני פסיכולוגים",
    "התניות",
    "התניות על מועמדים",
    "זמני מועמדים",
  ];

  const createFormFiles = formLabels.map((label) => {
    return (
      <>
        <Form.Label>{`${label}:`}</Form.Label>
        <Form.Control
          onChange={(e) => {
            handleChangeFile(e);
          }}
          required
          type="file"
        />
      </>
    );
  });

  return (
    <div>
      <Modal
        rtl={true}
        {...props}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter "
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">
            בניית לו"ז:
          </Modal.Title>
        </Modal.Header>
        {props.showerror === true ? (
          <Alert variant={"danger"}>הפעולה נכשלה</Alert>
        ) : undefined}
        <Modal.Body>
          <Form noValidate validated={validated} onSubmit={handleSubmit}>
            <Form.Group controlId="formFile" className="mb-3">
              {createFormFiles}
            </Form.Group>
            {!isLoading ? (
              <Button variant="primary" type="submit">
                הכן לו"ז
              </Button>
            ) : (
              <SpinnerInfinity
                size={50}
                thickness={100}
                speed={100}
                color="rgba(57, 77, 172, 1)"
                secondaryColor="rgba(0, 0, 0, 0.44)"
              />
            )}
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
