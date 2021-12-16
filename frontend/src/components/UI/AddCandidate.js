import { Button, Modal, Form, Alert } from "react-bootstrap";
import { useState, useEffect } from "react";

const staticData = [
  {
    ranks: ["1", "2"],
    day: "ראשון",
    hour: "14:00",
    psychologist: "פסיכולוג3",
    id: 10,
  },
  {
    ranks: ["1"],
    day: "שני",
    hour: "16:00",
    psychologist: "פסיכולוג5",
    id: 11,
  },
  {
    ranks: ["1", "2"],
    day: "שלישי",
    hour: "17:00",
    psychologist: "פסיכולוג8",
    id: 12,
  },
  {
    ranks: ["1", "2", "3"],
    day: "רביעי",
    hour: "19:00",
    psychologist: "פסיכולוג1",
    id: 13,
  },
  {
    ranks: ["1", "2", "3"],
    day: "חמישי",
    hour: "11:00",
    psychologist: "פסיכולוג1",
    id: 14,
  },
  {
    ranks: ["1"],
    day: "שני",
    hour: "07:00",
    psychologist: "פסיכולוג4",
    id: 14,
  },
  {
    ranks: ["1", "2"],
    day: "ראשון",
    hour: "10:00",
    psychologist: "פסיכולוג3",
    id: 15,
  },
];

const AddCandidate = (props) => {
  const [validated, setValidated] = useState(false);
  const [showRows, setShowRows] = useState([]);

  const [selectedOption, setSelectedOption] = useState(staticData[0].id);
  const [level, setLevel] = useState("1");

  useEffect(() => {
    const options = staticData.filter((item) => {
      return true === item.ranks.includes(level);
    });
    const showOptions = options.map((option) => {
      return (
        <option
          value={`${option.id}`}
        >{`${option.psychologist} - ${option.day} - ${option.hour}`}</option>
      );
    });
    setShowRows(showOptions);
  }, []);
  const handleSubmit = (event) => {
    const form = event.currentTarget;
    if (form.checkValidity() === false) {
      event.preventDefault();
      event.stopPropagation();
      setValidated(true);
    } else {
      event.preventDefault();
      const arr = staticData.filter((item) => {
        return item.id == selectedOption;
      });
      const add = arr[0];
      console.log(arr);
      const newCandidate = {
        candidate: event.target.fullname.value,
        day: add.day,
        hour: add.hour,
        psychologist: add.psychologist,
        id: add.id,
      };
      const newData = props.data;
      newData.push(newCandidate);
      props.editdata(newData);
      props.onHide();
    }
  };

  const handleChangeLevel = (e) => {
    e.preventDefault();
    const val = e.target.value;
    //get all the lines that can worked in this rank
    setLevel(val);
    const options = staticData.filter((item) => {
      return true === item.ranks.includes(val);
    });
    const showOptions = options.map((option) => {
      return (
        <option
          value={`${option.id}`}
        >{`${option.psychologist} - ${option.day} - ${option.hour}`}</option>
      );
    });
    setShowRows(showOptions);
  };
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
            :הוספת מועמד
          </Modal.Title>
        </Modal.Header>
        {props.showerror !== 0 && (
          <Alert variant={"danger"}>הפעולה נכשלה</Alert>
        )}
        <Modal.Body>
          <Form noValidate validated={validated} onSubmit={handleSubmit}>
            <Form.Group className="mb-3" controlId="fullname">
              <Form.Label>הזן שם</Form.Label>
              <Form.Control
                required
                type="text"
                defaultValue={props.data.text}
                placeholder=" ישראל ישראלי"
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="rankOptions">
              <Form.Select
                onChange={(e) => {
                  handleChangeLevel(e);
                }}
                disabled={false}
                aria-label="Default select example"
              >
                <Form.Text>Text</Form.Text>
                {/*the current sitution*/}
                <option value="DEFAULT" disabled>
                  בחר\י אפשרות
                </option>
                <option value="1">דרג א</option>
                <option value="2">דרג ב</option>
                <option value="3">דרג ג</option>
              </Form.Select>
            </Form.Group>

            <Form.Group className="mb-3" controlId="options">
              <Form.Select
                onChange={(e) => setSelectedOption(e.target.value)}
                aria-label="Default select example"
              >
                <Form.Text>Text</Form.Text>
                {/*the current sitution*/}
                <option value="DEFAULT" disabled>
                  בחר\י אפשרות
                </option>
                {showRows}
              </Form.Select>
            </Form.Group>

            <Button variant="success" type="submit">
              הוספה
            </Button>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button onClick={props.onHide}>סגירה</Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

export default AddCandidate;
