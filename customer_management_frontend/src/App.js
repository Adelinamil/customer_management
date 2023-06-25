import './App.css';
import {Navigate, Route, Routes} from "react-router-dom";
import {LoginPage} from "./pages/login";
import {getUser, useAccessToken} from "./functions/user";
import {MainPage} from "./pages/main";
import {CustomersPage} from "./pages/customers";
import {ProductsPage} from "./pages/products";
import {OrdersPage} from "./pages/orders";
import {EmployeesPage} from "./pages/employees";
import {Header} from "./components/header";
import moment from "moment";
import "moment/locale/ru";
import {useEffect, useState} from "react";

moment.locale('ru');

export const apiUrl = process.env.REACT_APP_API_URL;

function App() {
    const {accessToken, setAccessToken} = useAccessToken();
    const [user, setUser] = useState(null);
    useEffect(() => {
        const getAndSetUser = async () => {
            if (accessToken !== null) {
                const user = await getUser(accessToken);
                setUser(user);
            }
        };
        getAndSetUser().catch(console.error);
    }, [accessToken]);
    return (
        <div className="App">
            <header hidden={accessToken === null}>
                <Header setAccessToken={setAccessToken} user={user}/>
            </header>
            <main>
                <Routes>
                    <Route path={'/login'}
                           element={<LoginPage accessToken={accessToken} setAccessToken={setAccessToken}/>}/>
                    <Route path={'/'} element={<MainPage accessToken={accessToken}/>}/>
                    <Route path={'/customers'} element={<CustomersPage accessToken={accessToken}/>}/>
                    <Route path={'/products'} element={<ProductsPage accessToken={accessToken}/>}/>
                    <Route path={'/orders'} element={<OrdersPage accessToken={accessToken}/>}/>
                    <Route path={'/employees'} element={<EmployeesPage accessToken={accessToken} user={user}/>}/>
                    <Route path="*" element={<Navigate to="/" replace/>}/>
                </Routes>
            </main>
        </div>
    );
}

export default App;
