import {Container} from "react-bootstrap";
import {apiUrl} from "../App";
import DataTable from "react-data-table-component";
import {useEffect, useMemo, useState} from "react";
import {sendAPIRequest} from "../functions/requests";
import {Export} from "../components/export";
import {downloadCSV} from "../functions/export_to_csv";

const columns = [
    {
        name: 'ID',
        selector: row => row['id'],
        sortable: true
    },
    {
        name: 'Название',
        selector: row => row['title'],
        sortable: true,
        wrap: true
    },
    {
        name: 'Категория',
        selector: row => row['category'],
        sortable: true,
        wrap: true
    },
    {
        name: 'Бренд',
        selector: row => row['brand'],
        sortable: true,
        wrap: true
    },
    {
        name: 'Описание',
        selector: row => row['description']
    },
    {
        name: 'Цвет',
        selector: row => row['color'],
        sortable: true
    },
    {
        name: 'Размер',
        selector: row => row['size'],
        sortable: true
    },
    {
        name: 'Кол-во на складе',
        selector: row => row['in_stock'],
        sortable: true
    },
    {
        name: 'Изображение',
        selector: row => row['id'],
        cell: row => <a href={apiUrl + "/product/image/" + row["id"]}>Перейти</a>
    },
]

export const ProductsPage = (props) => {
    const [pending, setPending] = useState(true);
    const [products, setProducts] = useState([]);
    useEffect(() => {
        const getCustomers = async () => {
            const customers = await sendAPIRequest(props.accessToken, '/product/all');
            setProducts(customers);
            setPending(false);
        }
        getCustomers().catch(console.error);
    }, [props.accessToken]);
    const onProductClicked = (row, e) => {
    }
    const actionsMemo = useMemo(
        () => <Export onExport={() => downloadCSV('products', products)}/>,
        [products]
    );
    return (
        <Container>
            <DataTable responsive title="Товар" columns={columns} data={products} pagination
                       progressPending={pending} onRowClicked={onProductClicked}
                       actions={actionsMemo}
            />
        </Container>
    );
}