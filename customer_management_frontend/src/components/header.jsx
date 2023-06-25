import {Container, Nav, Navbar} from "react-bootstrap";
import {LinkContainer} from "react-router-bootstrap";
import {useNavigate} from "react-router-dom";
import {checkUserPermission} from "../functions/user";

export const Header = (props) => {
    const navigate = useNavigate();

    const logout = () => {
        props.setAccessToken(null);
        navigate('/login');
    }

    return (
        <Navbar bg="light" data-bs-theme="light">
            <Container>
                <LinkContainer to="/">
                    <Navbar.Brand>∞</Navbar.Brand>
                </LinkContainer>
                <Nav className="me-auto">
                    <LinkContainer to="/customers">
                        <Nav.Link>Клиенты</Nav.Link>
                    </LinkContainer>
                    <LinkContainer to="/products">
                        <Nav.Link>Продукты</Nav.Link>
                    </LinkContainer>
                    <LinkContainer to="/orders">
                        <Nav.Link>Заказы</Nav.Link>
                    </LinkContainer>
                    <LinkContainer to="/employees">
                        <Nav.Link
                            hidden={!checkUserPermission(props.user)}>
                            Сотрудники
                        </Nav.Link>
                    </LinkContainer>
                </Nav>
                <Nav>
                    <Nav.Link onClick={logout}>Выйти</Nav.Link>
                </Nav>
            </Container>
        </Navbar>
    );
}