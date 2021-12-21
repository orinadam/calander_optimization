import { Table } from "react-bootstrap";
import { useContext } from "react";
import { CandidateData } from "../../App";
const ScheduleTable = (props) => {
  const { candidate, setCandidate } = useContext(CandidateData);
  const openCandidateModal = (item) => {
    setCandidate(item);
    props.openCandidate();
  };
  const rows = props.data.map((item, i) => {
    return (
      <tr
        key={item.id}
        onClick={() => {
          openCandidateModal(item);
        }}
      >
        <th>{item.candidate}</th>
        <th>{item.day}</th>
        <th>{item.hour}</th>
        <th>{item.psychologist}</th>
      </tr>
    );
  });
  return (
    <Table rtl={true} striped bordered hover size="sm">
      <thead>
        <tr key={0}>
          <th>מועמדים</th>
          <th>יום</th>
          <th>שעה</th>
          <th>פסיכולוג</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </Table>
  );
};

export default ScheduleTable;
