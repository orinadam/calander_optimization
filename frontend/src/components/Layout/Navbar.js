
import axios from 'axios'
import 'bootstrap/dist/css/bootstrap.css';
import {Navbar, Container, Nav} from 'react-bootstrap'
import {useState} from 'react'
import { FcCalendar } from "react-icons/fc";
    

const NavbarHeader = (props) => {
    
    return <Navbar bg="success" variant="dark">
    <Container>
    <Navbar.Brand>מדור קצונה</Navbar.Brand>
    <Nav className="me-auto">
      <Nav.Link onClick={props.onClickForm}><FcCalendar/>יצירת לו"ז</Nav.Link>
    </Nav>
    </Container>
    
  </Navbar>

}

export default NavbarHeader;