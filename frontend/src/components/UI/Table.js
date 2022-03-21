import { Table, Form } from "react-bootstrap";
import { useContext, useState, useEffect } from "react";
import { CandidateData } from "../../App";
const ScheduleTable = (props) => {
  const { candidate, setCandidate } = useContext(CandidateData);
  const [ object, setObject] = useState({"id" : false})
  const [headerDisplay, setHeaderDisplay] = useState([])

const filterObjects = (e) =>
{
  e.preventDefault()
  console.log(e)
}

const changeValObject = (e) => {
  e.preventDefault()
}
const checkbox = props.headers.map((item) => {
    return  <span style={{margin : "10px"}}>
    <label>
      <input value={item} type="checkbox" onChange={(e) => {
        changeValObject(e)
      }}/>
      {item}
    </label>
  </span>
  })
const formButtons = () =>
{
  return <form>
    {checkbox}
    <button type="submit" onClick={(e) => {filterObjects(e)}}>סנן</button>
  </form>
}
const headersShow = props.headers.map((item) => {
  return <th>{item}</th>
})

  const openCandidateModal = (item) => {
    setCandidate(item);
    props.openCandidate();
  };

  useEffect(() => {
    let header_table = props.headers.map((item) => {
      return <th>{item}</th>;
    })
    setHeaderDisplay(header_table)
  }, []);
  const rows = props.data.map((item, i) => {
    var items = [];
    for (var i = 0; i < props.headers.length; i++) {
      items.push(<th>{item[props.headers[i]]}</th>);
    }
    return (
      <tr
        key={item.id}
      >
        {items}
      </tr>
    );
  });
  return (
    <div>
      {console.log(headerDisplay)}
    <Table rtl={true} striped bordered hover size="sm">
      <thead>
        <tr key={0}>{headersShow}</tr>
      </thead>
      <tbody>{rows}</tbody>
    </Table>
    </div>
  );
};

export default ScheduleTable;
