import {Button, ButtonGroup, Container, Form, Modal} from "react-bootstrap";
import DataTable from 'react-data-table-component';
import {useEffect, useMemo, useState} from "react";
import {sendAPIRequest, sendAPIRequestWithBody} from "../functions/requests";
import moment from "moment";
import {Export} from "../components/export";
import {downloadCSV} from "../functions/export_to_csv";
import {getInputChangeFunc} from "../functions/input_change";

const columns = [
    {
        name: 'ID',
        selector: row => row['id'],
        sortable: true,
        wrap: true
    },
    {
        name: 'Имя',
        selector: row => row['first_name'],
        sortable: true
    },
    {
        name: 'Фамилия',
        selector: row => row['second_name'],
        sortable: true
    },
    {
        name: 'Адрес',
        selector: row => row['address'],
        sortable: true,
        wrap: true
    },
    {
        name: 'Номер телефона',
        selector: row => row['phone_number'],
        sortable: true,
    },
    {
        name: 'Дата создания',
        selector: row => row['created'],
        sortable: true,
        format: row => moment(row['created']).format('lll'),
        wrap: true
    }
];


export const CustomersPage = (props) => {
    const [pending, setPending] = useState(true);
    const [showModal, setShowModal] = useState(false);
    const [showConfirmModal, setShowConfirmModal] = useState(false);
    const [customer, setCustomer] = useState(
        {"id": "", "first_name": "", "second_name": "", "address": "", "phone_number": ""}
    )
    const [customers, setCustomers] = useState([]);
    useEffect(() => {
        const getCustomers = async () => {
            const customers = await sendAPIRequest(props.accessToken, '/customer/all');
            setCustomers(customers);
            setPending(false);
        }
        getCustomers().catch(console.error);
    }, [pending, props.accessToken]);
    const actionsMemo = useMemo(
        () => <Export onExport={() => downloadCSV('customers', customers)}/>,
        [customers]
    );
    const clearCustomer = () => {
        setCustomer({"id": "", "first_name": "", "second_name": "", "address": "", "phone_number": ""});
    };
    const showCustomerModal = () => setShowModal(true);
    const hideCustomerModal = () => {
        setShowModal(false);
        clearCustomer();
    };
    const onClickCustomer = (row) => {
        setCustomer(row);
        showCustomerModal();
    };
    const onInputChange = getInputChangeFunc(setCustomer);

    const hideConfirmDeleteModal = () => setShowConfirmModal(false);
    const showConfirmDeleteModal = () => setShowConfirmModal(true);

    const onUpdateCustomer = async (e) => {
        e.preventDefault();
        await sendAPIRequestWithBody(
            props.accessToken,
            '/customer/update',
            JSON.stringify(customer),
            'PUT'
        );
        hideCustomerModal();
        setPending(true);
    };

    const onDeleteCustomer = async (e) => {
        e.preventDefault();
        await sendAPIRequest(
            props.accessToken,
            '/customer/' + customer.id,
            'DELETE'
        )
        hideConfirmDeleteModal();
        hideCustomerModal();
        setPending(true);
    };

    return (
        <Container className="mt-2">
            <DataTable responsive title="Клиенты" columns={columns} data={customers} pagination
                       progressPending={pending} actions={actionsMemo} onRowClicked={onClickCustomer}/>
            <Modal centered show={showModal} onHide={hideCustomerModal} style={{background: "rgba(0, 0, 0, 0.3)"}}>
                <Modal.Header closeButton>
                    <Modal.Title>Клиент</Modal.Title>
                </Modal.Header>
                <Form onSubmit={onUpdateCustomer}>
                    <Modal.Body>
                        <Form.Control autoComplete="off" className="mt-3" type="text" name="first_name"
                                      placeholder="Имя"
                                      maxLength={100}
                                      value={customer.first_name}
                                      onChange={onInputChange}
                                      required/>
                        <Form.Control autoComplete="off" className="mt-3" type="text" name="second_name"
                                      placeholder="Фамилия"
                                      maxLength={100}
                                      value={customer.second_name}
                                      onChange={onInputChange}
                                      required/>
                        <Form.Control autoComplete="off" className="mt-3" type="text" name="address"
                                      placeholder="Адрес"
                                      maxLength={200}
                                      value={customer.address}
                                      onChange={onInputChange}
                                      required/>
                        <Form.Control autoComplete="off" className="mt-3" type="text" name="phone_number"
                                      placeholder="Номер телефона"
                                      maxLength={20}
                                      value={customer.phone_number}
                                      onChange={onInputChange}
                                      required/>
                    </Modal.Body>
                    <Modal.Footer>
                        <ButtonGroup className="w-100">
                            <Button onClick={showConfirmDeleteModal} className="bg-gradient"
                                    variant="danger">Удалить</Button>
                            <Button type="submit" className="bg-gradient" variant="primary">Сохранить</Button>
                        </ButtonGroup>
                    </Modal.Footer>
                </Form>
            </Modal>
            <Modal centered show={showConfirmModal} onHide={hideConfirmDeleteModal}
                   style={{background: "rgba(0, 0, 0, 0.4)"}}>
                <Modal.Header closeButton>
                    <Modal.Title>Удаление клиента</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                    Вы уверены, что хотите удалить клиента {customer.id}?
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="primary" onClick={onDeleteCustomer}>
                        Да, удалить
                    </Button>
                    <Button variant="danger" onClick={hideConfirmDeleteModal}>
                        Нет, назад
                    </Button>
                </Modal.Footer>
            </Modal>
        </Container>
    );
}