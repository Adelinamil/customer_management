import {Button, ButtonGroup, Form, Modal} from "react-bootstrap";


export const EmployeeModal = (props) => {
    return (
        <>
            <Modal centered show={props.show} onHide={props.onHide}
                   style={{background: "rgba(0, 0, 0, 0.3)"}}>
                <Modal.Header closeButton>
                    <Modal.Title>Сотрудник</Modal.Title>
                </Modal.Header>
                <Form onSubmit={props.onSubmit}>
                    <Modal.Body>
                        <Form.Control autoComplete="off" className="mt-3" type="text" name="username"
                                      placeholder="Логин"
                                      maxLength={32}
                                      value={props.employee.username}
                                      minLength={3}
                                      onChange={props.onChange}
                                      required={props.create}/>
                        <Form.Control autoComplete="off" className="mt-3" type="password" name="password"
                                      placeholder="Пароль"
                                      maxLength={32}
                                      minLength={5}
                                      value={props.employee.password}
                                      onChange={props.onChange}
                                      required={props.create}/>
                        <Form.Control autoComplete="off" className="mt-3" type="text" name="first_name"
                                      placeholder="Имя"
                                      maxLength={100}
                                      minLength={2}
                                      value={props.employee.first_name}
                                      onChange={props.onChange}
                                      required={props.create}/>
                        <Form.Control autoComplete="off" className="mt-3" type="text" name="second_name"
                                      placeholder="Фамилия"
                                      maxLength={100}
                                      value={props.employee.second_name === null ? "" : props.employee.second_name}
                                      onChange={props.onChange}/>
                        <Form.Control hidden={props.create} className="mt-3" type="text" name="user_type"
                                      placeholder={props.employee.user_type}
                                      aria-label={props.employee.user_type}
                                      disabled
                                      required={props.create}/>
                        <Form.Select onChange={props.onChange} className="mt-3" hidden={!props.create}
                                     aria-label="Должность" name="user_type">
                            {props.userTypesOptions.map((option, index) => (
                                <option key={index} value={option.value}>{option.label}</option>
                            ))}
                        </Form.Select>
                        <small className="m-auto text-danger">
                            {props.error}
                        </small>
                    </Modal.Body>
                    <Modal.Footer>
                        <ButtonGroup className="w-100">
                            <Button hidden={props.create} onClick={props.showConfirmDeleteModal}
                                    className="bg-gradient"
                                    variant="danger">Удалить</Button>
                            <Button type="submit" className="bg-gradient" variant="primary">Сохранить</Button>
                        </ButtonGroup>
                    </Modal.Footer>
                </Form>
            </Modal>
            <Modal centered show={props.showConfirmModal} onHide={props.hideConfirmModal}
                   style={{background: "rgba(0, 0, 0, 0.4)"}}>
                <Modal.Header closeButton>
                    <Modal.Title>Удаление сотрудника</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    Вы уверены, что хотите удалить клиента {props.employee.id}?
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="primary" onClick={props.onDeleteEmployee}>
                        Да, удалить
                    </Button>
                    <Button variant="danger" onClick={props.hideConfirmModal}>
                        Нет, назад
                    </Button>
                </Modal.Footer>
            </Modal>
        </>
    );
}