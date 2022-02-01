import { Table } from "react-bootstrap";
import { useContext } from "react";
import { CandidateData } from "../../App";
const ScheduleTable = (props) => {
  const { candidate, setCandidate } = useContext(CandidateData);
  const openCandidateModal = (item) => {
    setCandidate(item);
    props.openCandidate();
  };
  const header_table = props.headers.map((item) => {
    return <th>{item}</th>;
  });
  const rows = props.data.map((item, i) => {
    var items = [];
    for (var i = 0; i < props.headers.length; i++) {
      items.push(<th>{item[props.headers[i]]}</th>);
    }
    return (
      <tr
        key={item.id}
        onClick={() => {
          openCandidateModal(item);
        }}
      >
        {items}
      </tr>
    );
  });
  return (
    <Table rtl={true} striped bordered hover size="sm">
      <thead>
        <tr key={0}>{header_table}</tr>
      </thead>
      <tbody>{rows}</tbody>
    </Table>
  );
};

export default ScheduleTable;
