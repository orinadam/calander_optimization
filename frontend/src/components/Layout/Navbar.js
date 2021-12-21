import axios from "axios";
import "bootstrap/dist/css/bootstrap.css";
import { Navbar, Container, Nav, Row, Col } from "react-bootstrap";
import { useState } from "react";
import { FcCalendar } from "react-icons/fc";

const NavbarHeader = (props) => {
  return (
    <Navbar bg="success" variant="dark">
      <Container>
        <Row>
          <Col>
            <Navbar.Brand>מדור קצונה</Navbar.Brand>
          </Col>
          <Col>
            <Nav className="auto">
              <Nav.Link onClick={props.onClickForm}>
                יצירת לו"ז
                <FcCalendar />
              </Nav.Link>
            </Nav>
          </Col>
        </Row>
      </Container>
    </Navbar>
  );
};

export default NavbarHeader;
