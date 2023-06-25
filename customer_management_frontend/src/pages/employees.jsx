import {Button, Container} from "react-bootstrap";
import {getUserType} from "../functions/utils";
import moment from "moment";
import {useEffect, useMemo, useState} from "react";
import {sendAPIRequest, sendAPIRequestWithBody} from "../functions/requests";
import DataTable from "react-data-table-component";
import {checkUserPermission} from "../functions/user";
import {getInputChangeFunc} from "../functions/input_change";
import {EmployeeModal} from "../components/forms/employee_modal";

const columns = [
    {
        name: 'ID',
        selector: row => row['id'],
        sortable: true,
        wrap: true
    },
    {
        name: 'Логин',
        selector: row => row['username'],
        sortable: true,
        wrap: true
    },
    {
        name: 'Должность',
        selector: row => row['user_type'],
        sortable: true,
        format: row => getUserType(row['user_type'])
    },
    {
        name: 'Имя',
        selector: row => row['first_name'],
        sortable: true,
        wrap: true
    },
    {
        name: 'Фамилия',
        selector: row => row['second_name'],
        sortable: true,
        wrap: true
    },
    {
        name: 'Последняя активность',
        selector: row => row['last_activity'],
        sortable: true,
        format: row => moment(row['created']).format('lll'),
        wrap: true
    },
    {
        name: 'Дата создания',
        selector: row => row['created'],
        sortable: true,
        format: row => moment(row['created']).format('lll'),
        wrap: true
    },
];

export const EmployeesPage = (props) => {
    const [pending, setPending] = useState(true);
    const [create, setCreate] = useState(false);
    const [showModal, setShowModal] = useState(false);
    const [showConfirmModal, setShowConfirmModal] = useState(false);
    const [employee, setEmployee] = useState(
        {"id": "", "username": "", "password": "", "user_type": "", "first_name": "", "second_name": ""}
    );
    const [employees, setEmployees] = useState([]);
    const [error, setError] = useState("");
    const [userTypes, setUserTypes] = useState([]);
    useEffect(() => {
        const getCustomers = async () => {
            const employees_resp = await sendAPIRequest(props.accessToken, '/user/all');
            setEmployees(employees_resp);
            const user_types = await sendAPIRequest(props.accessToken, '/user/types');
            setUserTypes(user_types.filter(item => !['developer', 'admin'].includes(item)));
            setPending(false);
        }
        getCustomers().catch(console.error);
    }, [pending, props.accessToken]);

    const clearEmployee = () => {
        setEmployee({"id": "", "username": "", "password": "", "user_type": "", "first_name": "", "second_name": ""});
    };

    const hideEmployeeModal = () => {
        setShowModal(false);
        clearEmployee();
    };
    const showEmployeeModal = () => setShowModal(true);

    const onClickEmployee = (row) => {
        setCreate(false);
        if (['seller', 'manager'].includes(row.user_type)) {
            setEmployee({
                "id": row["id"],
                "username": row["username"],
                "password": "",
                "user_type": row["user_type"],
                "first_name": row["first_name"],
                "second_name": row["second_name"]
            });
            showEmployeeModal();
        }
    };

    const hideConfirmModal = () => setShowConfirmModal(false);
    const showConfirmDeleteModal = () => setShowConfirmModal(true);

    const onCreateEmployee = async (e) => {
        e.preventDefault();
        const result = await sendAPIRequestWithBody(
            props.accessToken,
            '/user/create',
            JSON.stringify(employee),
            'POST'
        );
        if (result === true) {
            hideConfirmModal();
            hideEmployeeModal();
            setPending(true);
        } else {
            setError(result.detail);
        }
    };

    const onUpdateEmployee = async (e) => {
        e.preventDefault();
        await sendAPIRequestWithBody(
            props.accessToken,
            '/user/update',
            JSON.stringify({
                "id": employee.id,
                "username": employee.username === "" ? null : employee.username,
                "password": employee.password === "" ? null : employee.password,
                "first_name": employee.first_name === "" ? null : employee.first_name,
                "second_name": employee.second_name === "" ? null : employee.second_name
            }),
            'PUT'
        );
        hideEmployeeModal();
        setPending(true);
    };
    const onDeleteEmployee = async (e) => {
        e.preventDefault();
        await sendAPIRequest(
            props.accessToken,
            '/user/' + employee.id,
            'DELETE'
        )
        hideConfirmModal();
        hideEmployeeModal();
        setPending(true);
    };

    const onInputChange = getInputChangeFunc(setEmployee);


    const actionsMemo = useMemo(
        () => <Button className="rounded" size="sm" onClick={() => {
            setCreate(true);
            setEmployee(prev => ({...prev, "user_type": "seller"}));
            showEmployeeModal();
        }}>Добавить</Button>, []
    );

    const userTypesOptions = userTypes.map((userType) => {
        return {value: userType, label: getUserType(userType)};
    })
    if (!checkUserPermission(props.user)) {
        return <Container className="p-5 text-center"><h1>403 Forbidden</h1></Container>;
    } else {
        return (
            <Container>
                <DataTable responsive title="Сотрудники" columns={columns} data={employees} pagination
                           progressPending={pending} actions={actionsMemo} onRowClicked={onClickEmployee}/>
                <EmployeeModal
                    show={showModal}
                    onHide={hideEmployeeModal}
                    employee={employee}
                    onChange={onInputChange}
                    showConfirmDeleteModal={showConfirmDeleteModal}
                    showConfirmModal={showConfirmModal}
                    hideConfirmModal={hideConfirmModal}
                    onDeleteEmployee={onDeleteEmployee}
                    create={create}
                    onSubmit={create ? onCreateEmployee : onUpdateEmployee}
                    error={error}
                    userTypesOptions={userTypesOptions}
                />
            </Container>
        );
    }
};