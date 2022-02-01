import Navbar from "./components/Layout/Navbar";
import UploadFilesModal from "./components/UI/UploadFilesModal";
import { useState } from "react";
import ScheduleTable from "./components/UI/Table";
import EditCandidate from "./components/UI/EditCandidate";
import { useMemo, createContext, useEffect } from "react";
import { Card, Button } from "react-bootstrap";
import AddCandidate from "./components/UI/AddCandidate";
import exportFromJSON from "export-from-json";
import "./App.css";
import axios from "axios";

const fileName = "download";
const exportType = "xls";

//until we will connect the front with the back
const staticData = [
  {
    candidate: "מועמד1",
    day: "ראשון",
    hour: "13:00",
    psychologist: "פסיכולוג2",
    id: 1,
  },
  {
    candidate: "מועמד2",
    day: "שני",
    hour: "14:00",
    psychologist: "פסיכולוג3",
    id: 2,
  },
  {
    candidate: "מועמד3",
    day: "ראשון",
    hour: "13:00",
    psychologist: "פסיכולוג1",
    id: 3,
  },
  {
    candidate: "מועמד4",
    day: "שלישי",
    hour: "12:00",
    psychologist: "פסיכולוג2",
    id: 4,
  },
  {
    candidate: "מועמד5",
    day: "חמישי",
    hour: "15:00",
    psychologist: "פסיכולוג3",
    id: 5,
  },
  {
    candidate: "מועמד6",
    day: "ראשון",
    hour: "13:00",
    psychologist: "פסיכולוג1",
    id: 6,
  },
];

export const CandidateData = createContext({
  candidate: {},
  setCandidate: () => {},
});

function App() {
  //Upload Files
  const [formModal, setFormModal] = useState(false);
  const [errorModal, setErrorModal] = useState(false);

  const [headers, setHeaders] = useState([]);
  //Schedule
  const [data, setData] = useState([]);
  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/check")
      .then((res) => {
        var headers = res["data"].data.slice(0, 1)[0];
        var data = res["data"].data.slice(1, res["data"].data.length);
        var obj = [];
        for (var i = 0; i < data.length; i++) {
          var temp = {};
          for (var j = 0; j < data[i].length; j++) {
            temp[headers[j]] = data[i][j];
          }
          obj.push(temp);
        }
        setData(obj);
        setHeaders(headers);
      })
      .catch((err) => {
        console.log(err);
      });
  }, []);

  //Edit Candidate Modal
  const [candidateModal, setCandidateModal] = useState(false);
  const [errorCandidateModal, setErrorCandidateModal] = useState(false);
  const [candidate, setCandidate] = useState({});

  //modal for adding a candidate to the schedule
  const [addCandidateModal, setAddCandidateModal] = useState(false);
  const [errorAddCandidateModal, setErrorAddCandidateModal] = useState(false);

  const closeModal = (errFunc, formFunc) => {
    errFunc(false);
    formFunc(false);
  };

  const exportToExcel = () => {
    exportFromJSON({ data, fileName, exportType });
  };
  const deleteTable = () => {
    setData([]);
  };
  const value = useMemo(() => ({ candidate, setCandidate }), [candidate]);
  return (
    <div>
      <CandidateData.Provider value={value}>
        {/*header*/}
        <Navbar
          onClickForm={() => {
            setFormModal(true);
          }}
        />
        {/*modals*/}
        {formModal && (
          <UploadFilesModal
            changerrror={setErrorModal ? 1 : 0}
            showerror={errorModal}
            data={data}
            editdata={setData}
            show={formModal}
            onHide={() => {
              closeModal(setErrorModal, setFormModal);
            }}
          />
        )}
        {candidateModal && (
          <EditCandidate
            data={data}
            editdata={setData}
            changeerror={() => {
              setErrorCandidateModal();
            }}
            showerror={errorCandidateModal ? 1 : 0}
            show={candidateModal}
            onHide={() => {
              closeModal(setErrorModal, setCandidateModal);
            }}
          />
        )}
        {addCandidateModal && (
          <AddCandidate
            data={data}
            editdata={setData}
            changeerror={() => {
              setErrorAddCandidateModal();
            }}
            showerror={errorAddCandidateModal ? 1 : 0}
            show={addCandidateModal}
            onHide={() => {
              closeModal(setErrorAddCandidateModal, setAddCandidateModal);
            }}
          />
        )}

        {/*body*/}
        <br />
        <Card body>
          <Button onClick={exportToExcel} variant="outline-primary">
            הורדת טבלה
          </Button>{" "}
          <Button onClick={deleteTable} variant="outline-danger">
            מחיקת טבלה
          </Button>{" "}
          <Button
            onClick={() => {
              setAddCandidateModal(true);
            }}
            variant="outline-success"
          >
            הוספת מועמד
          </Button>{" "}
          <Button
            onClick={() => {
              console.log("upload file");
            }}
            variant="outline-secondary"
          >
            העלאת טבלה
          </Button>{" "}
        </Card>
        <br />
        {data.length !== 0 && (
          <ScheduleTable
            openCandidate={() => {
              setCandidateModal(true);
            }}
            data={data}
            headers={headers}
            editdata={() => {
              setData();
            }}
          />
        )}
      </CandidateData.Provider>
    </div>
  );
}

export default App;