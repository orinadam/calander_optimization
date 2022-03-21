

import { Button, Form } from "react-bootstrap";
import { useState, useContext } from "react";
import axios from "axios";



const LuzAuthPage = (props) => {

const handleSubmitUpdate = (event) => {
    event.preventDefault()
    fetch(`http://127.0.0.1:5000/luz?authority=${event.target.elements["authority"].value}`, {
        method: "GET",
      })
        .then(async (res) => {
          let data = await res.json();
          if(data["error"] !== "")
          {
            console.log("SOMETHING WRONG HAPPENED")
          }
          else
          {
            if(data["isempty"] === "true")
            {
                props.editdata([[]]);
                props.editheaders([[]]);
            }else{
            var headers = data["data"].slice(0, 1)[0]
            data = data["data"].slice(1, data["data"].length)

            var obj = [];
            for (var i = 0; i < data.length; i++) {
              var temp = {};
              for (var j = 0; j < data[i].length; j++) {
                temp[headers[j]] = data[i][j];
              }
              console.log(temp)
              obj.push(temp);
            }
            props.editdata(obj);
            props.editheaders(headers);
          }}
          })
          .catch((err) => {
            console.log(err);
          });

    
}

  return (
    <span rtl="true" > 
<Form onSubmit={(e) => {handleSubmitUpdate(e)}}>
  <Form.Group className="mb-3" controlId="formBasicText">
    <Form.Label>חיפוש לפי סמכות:</Form.Label>
    <Form.Control type="text" name="authority" placeholder="הזן סמכות" />
  </Form.Group>
  <Form.Group className="mb-3" controlId="formBasicCheckbox">
  </Form.Group>
  <Button variant="primary" type="submit">
    סנן
  </Button>
  
</Form>
<br/>
    </span>
  );
};

export default LuzAuthPage;
