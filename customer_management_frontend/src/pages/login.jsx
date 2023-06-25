import {Container} from "react-bootstrap";
import {LoginForm} from "../components/forms/login_form";
import {Navigate} from "react-router-dom";

export const LoginPage = (props) => {
    if (props.accessToken)
        return <Navigate to="/" replace/>;
    return (
        <div className="d-flex justify-content-center align-items-center" style={{height: '100vh'}}>
            <Container className="p-4 w-50">
                <h4 className="text-center">Пожалуйста, авторизируйтесь</h4>
                <LoginForm setAccessToken={props.setAccessToken}/>
            </Container>
        </div>
    );
};