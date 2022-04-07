import { Button, Modal } from "react-bootstrap";
import axios from "axios"


const DeleteTablePage = (props) => {
    const handleDeleteTable = (e) =>
    {
      e.preventDefault()
      axios.get("http://127.0.0.1:5000/cleantable")
      .then(res => {
        props.editHeaders([])
        props.editdata([])
      }).catch(err => {
        console.log(err)
      })
      props.onHide()
    }
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
          <Modal.Title id="contained-modal-title-vcenter">
              בטוח?
          </Modal.Title>
          <br/>
<Button onClick={handleDeleteTable}>כן</Button>{"  "}
<br/>
{"  "}<Button onClick={props.onHide}>לא</Button>{"  "}

        </Modal.Header>

      </Modal>
    </div>
  );
};

export default DeleteTablePage;
