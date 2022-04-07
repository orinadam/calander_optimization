import { Button, Modal, Form, Alert } from "react-bootstrap";
import { useState, useEffect } from "react";
import "./modify.css";
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
    id: 15,
  },
  {
    ranks: ["1", "2"],
    day: "ראשון",
    hour: "10:00",
    psychologist: "פסיכולוג3",
    id: 16,
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
    setSelectedOption(options[0].id);
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
    <div className="btn-close">
      <Modal
        rtl={true}
        {...props}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter "
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">
            הוספת מועמד:
          </Modal.Title>
        </Modal.Header>
        {props.showerror !== 0 && (
          <Alert variant={"danger"}>הפעולה נכשלה</Alert>
        )}
        <Modal.Body>
          <Form noValidate validated={validated} onSubmit={handleSubmit}>
            <Form.Group className="mb-3" controlId="firstname">
              <Form.Label> הזן שם פרטי </Form.Label>
              <Form.Control
                required
                type="text"
                defaultValue={props.data.text}
                placeholder=" ישראל "
              />
            </Form.Group>
            <Form.Group className="mb-3" controlId="secondname">
              <Form.Label> הזן שם משפחה</Form.Label>
              <Form.Control
                required
                type="text"
                defaultValue={props.data.text}
                placeholder=" ישראלי "
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="personalnumber">
            <Form.Label> הזמן מספר אישי</Form.Label>
              <Form.Control
                required
                type="text"
                defaultValue={props.data.text}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="personalnumber">
            <Form.Label> הזמן מייל</Form.Label>
              <Form.Control
                required
                type="mail"
                defaultValue={props.data.text}
              />
            </Form.Group>

            <Form.Group className="mb-3" controlId="personalnumber">
            <Form.Label> הזמן  טלפון</Form.Label>
              <Form.Control
                required
                type="text"
                defaultValue={props.data.text}
              />
            </Form.Group>
            <span>
            <label for="notify">  הזן הערות  </label>
            <select id="notify" name="notify">
              <option value="א">א</option>
              <option value="ב">ב</option>
              <option value="ג">ג</option>
              <option value="ד">ד</option>
            </select>
            {"  "}
            <label for="dapar">  הזן דפר  </label>
            <select id="dapar" name="dapar">
              <option value="10">10</option>
              <option value="20">20</option>
              <option value="30">30</option>
              <option value="40">40</option>
              <option value="50">50</option>
              <option value="60">60</option>
              <option value="70">70</option>
              <option value="80">80</option>
              <option value="90">90</option>

            </select>
            {"  "}
            <label for="hebrew">  הזן סימול עברית  </label>
            <select id="hebrew" name="hebrew">
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
              <option value="6">6</option>
              <option value="7">7</option>
              <option value="8">8</option>

            </select>


            {"  "}
            <label for="years">  הזן שנות לימוד  </label>
            <select id="years" name="years">
              <option value="3">1</option>
              <option value="3">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
              <option value="6">6</option>
              <option value="7">7</option>
              <option value="8">8</option>
              <option value="9">9</option>
              <option value="10">10</option>
              <option value="11">11</option>
              <option value="12">12</option>


            </select>
            </span>
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
