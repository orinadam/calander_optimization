import {Table} from "react-bootstrap"
import { useState } from "react"



const ScheduleTable = props =>
{
    console.log(props)
    const rows = props.data.map((item, i) => {
        return (
            <tr onClick={props.openCandidate}>
                <th>{item.candidate}</th>
                <th>{item.day}</th>
                <th>{item.hour}</th>
                <th>{item.psychologist}</th>
            </tr>
        )
    })
    return (
    <Table striped bordered hover size="sm">
        <thead>
        <tr>
            <th>מועמדים</th>
            <th>יום</th>
            <th>שעה</th>
            <th>פסיכולוג</th>
        </tr>
        </thead>
        <tbody>
            {rows}
        </tbody>
  </Table>
 )
}

export default ScheduleTable