import { Table, Form } from "react-bootstrap";
import { useContext, useState, useEffect } from "react";
import { CandidateData } from "../../App";
import { FcFullTrash } from "react-icons/fc";

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

const handleDeleteCandidate = async (e, value) =>
{
  e.preventDefault()
  await fetch(`http://127.0.0.1:5000/deleteone?code=${value}`, {
    method: "GET",
  })
  .then( async(res) => {
      var newData = await props.data.filter(item =>
        {
          return item["מ.א"] !== value
        })

        console.log(newData)
        await props.editdata(newData)

  })
  .catch(err => {
    console.log(err)
  })
}
const formButtons = () =>
{
  return <form>
    {checkbox}
    <button type="submit" onClick={(e) => {filterObjects(e)}}>סנן</button>
  </form>
}
const headersShow = props.headers.filter((item) => {
  return item != "code"
}).map((item) => {
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
      if(props.headers[i] !== "code")
      {
        items.push(<th>{item[props.headers[i]]}</th>);
      }
    }
    let color = ""
    if(props.headers.includes("code"))
    {
      if(item["code"] === 1){
          color = "orange"
      }else if(item["code"] === 2)
      {
        color = "red"
      }
    }
    var index = props.headers.indexOf("מ.א")
    console.log(index)
    if(index !== -1)
    {
      items.push(<button onClick={(e) => handleDeleteCandidate(e, item[props.headers[index]])}><FcFullTrash/></button>)
    }
    return (
      <tr
        bgcolor={color}
        key={item.id}
      >
        {items}
      </tr>
    );
  });
  return (
    <div>
      {console.log(props.data)}
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
