import fs, { fstat } from 'fs';
import os from 'os';
import pem from 'pem';
import conf from '../config/server.json';
import path from 'path';
import https from 'https';
import busboy from 'busboy';
import { pathAllowed, getDir } from './lib/files';
import express from 'express';
import { e403, e404, e400 } from './lib/error';

pem.createCertificate({
    days: 1,
    selfSigned: true,
}, (err, keys) => {
    if (err) throw err;
    const app = express();

    app.get('/', (req, res) => {
        res.send('Hello World!');
    });

    app.get('/f/:path', async (req, res) => {
        let p = Buffer.from(req.params.path, 'base64').toString();
        if (!pathAllowed(p, conf.path)) return e403(req, res);
        p = path.join(conf.path, p);
        console.log(' f: ' + p);
        if (!fs.existsSync(p)) return e404(req, res);
        res.sendFile(p);
    });

    app.get('/fs/:path?', async (req, res) => {
        let dir = await getDir(Buffer.from(req.params.path||'', 'base64').toString(), conf.path);
        if (!dir) return res.send('{}');
        res.send(JSON.stringify({
            success: true,
            dir,
        }));
    });

    app.post('/u/:path', async (req, res) => {
        let bb = new busboy({ headers: req.headers, });
        bb.on('file', (finame, file, fname, enc, mime) => {
            let p = Buffer.from(req.params.path, 'base64').toString();
            if (!pathAllowed(p, conf.path)) return e403(req, res);
            p = path.join(conf.path, p);
            console.log(' u: ' + p);
            if (fs.existsSync(p)) return e400(req, res);
            file.pipe(fs.createWriteStream(p));
        });
        bb.on('field', (finame, val, finametrunc, valtrunc, enc, mime) => {
            console.log(`[${finame}]: ${val} ... `);
        });
        bb.on('finish', () => {
            res.writeHead(200, { 'Connection': 'close', });
            res.end();
        });
        return req.pipe(bb);
    });

    app.post('/mk/:path', async (req, res) => {
        let dir = Buffer.from(req.params.path, 'base64').toString();
        if (!pathAllowed(dir, conf.path)) return e403(req, res);
        dir = path.join(conf.path, dir);
        console.log('mk: ' + dir);
        fs.mkdirSync(dir);
        res.end();
    });

    app.get('/host', async (req, res) => {
        res.send(JSON.stringify({
            username: os.userInfo().username,
            hostname: os.hostname(),
            uptime: os.uptime(),
            os: os.type(),
            platform: os.platform(),
        }));
    });

    const srv = https.createServer({
        key: keys.serviceKey,
        cert: keys.certificate,
    }, app).listen(conf.port, conf.host, () => console.log(`[UKEY]: Listening on https://${conf.host}:${conf.port} ... `));

    function stopServer(err: any) {
        if (err instanceof Error) {
            console.log(err.stack);
        }
        console.log(`[UKEY]: SIGTERM / Exception: Stopping server ... `);
        srv.close();
    }
    
    process.on('uncaughtException', stopServer);
    process.on('SIGTERM', stopServer);
});