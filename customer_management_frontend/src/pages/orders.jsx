import {Container} from "react-bootstrap";
import {useNavigate} from "react-router-dom";
import moment from "moment";
import {useEffect, useMemo, useState} from "react";
import {sendAPIRequest} from "../functions/requests";
import DataTable from "react-data-table-component";
import {getStatusName} from "../functions/utils";
import {downloadCSV} from "../functions/export_to_csv";
import {Export} from "../components/export";


const getColumns = (navigate) => {
    return [
        {
            name: 'ID',
            selector: row => row['id'],
            sortable: true
        },
        {
            name: 'Клиент',
            selector: row => row['customer_id'],
            sortable: true,
            wrap: true
        },
        {
            name: 'Товар',
            selector: row => row['product_id'],
            sortable: true,
            cell: row => <span style={{'color': 'blue', 'cursor': 'pointer'}}
                               onClick={() => navigate('/product/' + row['product_id'])}>{row['product_id']}</span>
        },
        {
            name: 'Кол-во',
            selector: row => row['quantity'],
            sortable: true
        },
        {
            name: 'Сумма',
            selector: row => row['total_price']
        },
        {
            name: 'Статус',
            selector: row => row['status'],
            sortable: true,
            wrap: true,
            format: row => getStatusName(row['status'])
        },
        {
            name: 'Дата создания',
            selector: row => row['dt'],
            sortable: true,
            format: row => moment(row['created']).format('lll'),
            wrap: true
        }
    ]
}


export const OrdersPage = (props) => {
    const [pending, setPending] = useState(true);
    const [orders, setOrders] = useState([]);
    useEffect(() => {
        const getCustomers = async () => {
            const customers = await sendAPIRequest(props.accessToken, '/order/all');
            setOrders(customers);
            setPending(false);
        }
        getCustomers().catch(console.error);
    }, [props.accessToken]);

    const navigate = useNavigate();
    const columns = getColumns(navigate);
    const export_orders = orders.map(item => {
        delete item['customer'];
        delete item['product'];
        return item;
    });
    const actionsMemo = useMemo(
        () => <Export onExport={() => downloadCSV('orders', export_orders)}/>,
        [export_orders]
    );
    return (
        <Container>
            <DataTable responsive title="Заказы" columns={columns} data={orders} pagination
                       progressPending={pending} actions={actionsMemo}/>
        </Container>
    );
}