export const getStatusName = (status) => {
    switch (status) {
        case "pending":
            return "Ожидает обработки";
        case "processing":
            return "В обработке";
        case "shipped":
            return "Отправлен";
        case "delivered":
            return "Доставлен";
        case "cancelled":
            return "Отменен";
        default:
            return "Неизвестно";
    }
};


export const getUserType = (user_type) => {
    switch (user_type) {
        case "seller":
            return "Продавец";
        case "manager":
            return "Менеджер";
        case "admin":
            return "Администратор";
        case "developer":
            return "Разработчик";
        default:
            return "Без статуса";
    }
};

