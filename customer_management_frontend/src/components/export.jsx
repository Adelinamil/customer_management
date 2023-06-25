import {Button} from "react-bootstrap";

export const Export = ({onExport}) => {
    return <Button className="rounded" size="sm" variant="primary" onClick={e => onExport(e.target.value)}>
        Экспорт данных
    </Button>;
}