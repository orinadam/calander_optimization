import { Button, Modal, Form, Alert } from "react-bootstrap";
import LuzAuthPage from "../LuzAuth";
import SearchAuthrity from "../SearchAutority";
import FindReplacementPage from "../FindReplacement";
import SpecificMeeting from "../SpecificMeetingPage";
import DaysPage from "../DaysSort";
const StaticData = [
  { day: "שני", hour: "11:00", psychologist: "פסיכולוג4" },
  { day: "ראשון", hour: "18:00", psychologist: "פסיכולוג1" },
  { day: "שישי", hour: "08:00", psychologist: "פסיכולוג3" },
];
/*
        {filterModal && (
          <FiltersModal
            changerrror={setErrorModal}
            showerror={errorModal}
            data={data}
            editdata={setData}
            headers={headers}
            editheaders={setHeaders}
            show={filterModal}
            onHide={() => {
              closeModal(setErrorModal, setFilterModal);
            }}
          />

        data={data}
          editdata={setData}
          headers={headers}
          editheaders={setHeaders}


*/
const EditCandidate = (props) => {
  return (
    <div>
      <Modal
        {...props}
        rtl={true}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter "
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">:פילטרים</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <SearchAuthrity
            data={props.data}
            editdata={props.editdata}
            headers={props.headers}
            editheaders={props.editheaders}
          />
          <SpecificMeeting
            data={props.data}
            editdata={props.editdata}
            headers={props.headers}
            editheaders={props.editheaders}
          />
          <LuzAuthPage
            data={props.data}
            editdata={props.editdata}
            headers={props.headers}
            editheaders={props.editheaders}
          />
          <DaysPage
            data={props.data}
            editdata={props.editdata}
            headers={props.headers}
            editheaders={props.editheaders}
          />

        </Modal.Body>
        <Modal.Footer>
          <Button onClick={props.onHide}>סגירה</Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
};

/*

          <FindReplacementPage
            data={props.data}
            editdata={props.editdata}
            headers={props.headers}
            editheaders={props.editheaders}
          />
*/
export default EditCandidate;
