import {Navigate} from "react-router-dom";
import {Container} from "react-bootstrap";


export const MainPage = (props) => {
    if (!props.accessToken)
        return <Navigate to="/login" replace/>;
    return (
        <Container>
            <h2>Dashboard</h2>
        </Container>
    );
}