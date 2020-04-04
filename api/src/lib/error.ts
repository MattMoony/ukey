export function e400(req, res) {
    res.status(400).send('Error 400 - Bad request!');
}

export function e403(req, res) {
    res.status(403).send('Error 403 - Not allowed!');
}

export function e404(req, res) {
    res.status(404).send('Error 404 - Resource not found!');
}

export function e500(req, res) {
    res.status(500).send('Error 500 - Internal Server Error!');
}