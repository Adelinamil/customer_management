import {Button, Form} from "react-bootstrap";
import {getInputChangeFunc} from "../../functions/input_change";
import {useState} from "react";
import {useNavigate} from "react-router-dom";
import {apiUrl} from "../../App";

export const LoginForm = (props) => {
    const [input, setInput] = useState({username: "", password: ""});
    const [error, setError] = useState({detail: ""});
    const onInputChange = getInputChangeFunc(setInput);
    const navigate = useNavigate();
    const onSubmit = (e) => {
        e.preventDefault();
        const body = new FormData();
        body.append("username", input.username);
        body.append("password", input.password);
        const requestParams = {
            method: "POST",
            body: body
        };
        fetch(apiUrl + "/user/login", requestParams).then((response) => response.json())
            .then(async (data) => {
                const detail = data["detail"];
                if (detail) {
                    setError({detail: detail});
                } else {
                    const token_type = data["token_type"];
                    const token = data["access_token"];
                    props.setAccessToken(`${token_type} ${token}`);
                    navigate({pathname: "/"});
                }
            });
    }

    return (
        <Form onSubmit={onSubmit} className="p-4 form">
            <Form.Group controlId="formUsername">
                <Form.Label>Логин</Form.Label>
                <Form.Control onChange={onInputChange} type="text" name="username" placeholder="example@mail.ru"
                              maxLength={32}
                              required/>
            </Form.Group>
            <br/>
            <Form.Group controlId="formPassword">
                <Form.Label>Пароль</Form.Label>
                <Form.Control onChange={onInputChange} type="password" name="password" placeholder="*****"
                              maxLength={32} required/>
            </Form.Group>
            <br/>
            <span className="text-danger small">
                {error.detail}
            </span>
            <Button className="bg-gradient w-100" variant="primary" type="submit">
                Войти
            </Button>
        </Form>
    );
}