import os from 'os';
import ip from 'ip';
import fs from 'fs';
import path from 'path';
import http from 'http';
import ftype from 'file-type';
import express from 'express';
import nunjucks from 'nunjucks';
import socketio from 'socket.io';
import diskusage from 'diskusage';
import conf from '../config/server.json';

const VPATH = path.join(__dirname, '../public/');

const app = express();
const srv = http.createServer(app);
const io = socketio(srv);

var conns = [];

nunjucks.configure(VPATH, {
    autoescape: true,
    express: app,
    noCache: true,
});
app.set('view engine', 'html');

// --- <ENDPOINTS> -------------------------------------------------------------------------------------------------------------------------------- //

app.get('/', (req, res) => {
    try {
        res.render('index', {
            host: getHostInfo(),
            disk: diskusage.checkSync(conf.path),
        });
    } catch (e) {
        e500(req, res);
    }
});

app.get('/files/:path?', async (req, res) => {
    let dir = await getDir(Buffer.from(req.params.path||'', 'base64').toString());
    if (!dir) return e404(req, res);
    res.render('files', {
        host: getHostInfo(),
        dir: JSON.stringify(dir),
    });
});

app.get('/f/:path', async (req, res) => {
    let p = Buffer.from(req.params.path, 'base64').toString();
    if (!pathAllowed(p)) return e404(req, res);
    p = path.join(conf.path, p);
    if (!fs.existsSync(p)) return e404(req, res);
    res.sendFile(p);
});

app.get('/fs/:path?', async (req, res) => {
    let dir = await getDir(Buffer.from(req.params.path||'', 'base64').toString());
    if (!dir) return res.send('{}');
    res.send(JSON.stringify({
        success: true,
        dir,
    }));
});

app.use('/', express.static(path.join(__dirname, '../public')));
app.use(/^\/(.+)/, e404);

srv.listen(conf.port, conf.host, () => console.log(`[UKEY]: Listening on ${conf.host}:${conf.port} ... `));

// --- </ENDPOINTS> ------------------------------------------------------------------------------------------------------------------------------- //

setInterval(async () => {
    if (conns.length > 0) {
        let inf = await cpuUsage();
        io.emit('resources', {
            cpuUsage: inf,
            ramUsage: 1-os.freemem()/os.totalmem(),
        });
    }
}, conf.emitPause);

io.on('connection', sock => {
    conns.push(sock.conn.remoteAddress);
    console.log(`[socket.io]: ${sock.conn.remoteAddress} connected ... `);
    sock.on('disconnect', () => {
        conns = [...conns.slice(0,conns.indexOf(sock.conn.remoteAddress)), ...conns.slice(conns.indexOf(sock.conn.remoteAddress)+1)]
        console.log(`[socket.io]: ${sock.conn.remoteAddress} disconnected ... `);
    });
});

function e404(req, res) {
    res.render('404', {
        path: req.params[0],
    });
}

function e500(req, res) {
    res.send('Error 500: Internal Server Error! (Try refreshing the page later ...)');
}

function _cpuUsage(stat1: os.CpuInfo, stat2: os.CpuInfo) {
    let idle = stat2.times.idle - stat1.times.idle;
    let tota = (stat2.times.idle + stat2.times.irq + stat2.times.nice + stat2.times.sys + stat2.times.user) - (stat1.times.idle + stat1.times.irq + stat1.times.nice + stat1.times.sys + stat1.times.user);
    return 1-idle/tota;
}

function cpuUsage() {
    return new Promise(res => {
        let stats1 = os.cpus();
        setTimeout(() => {
            let stats2 = os.cpus();
            res(stats2.map((s, i) => _cpuUsage(stats1[i], s)));
        }, 1000);
    });
}

function _pathAllowed(subPath, parPath) {
    let tp = path.join(parPath, subPath);
    return tp.startsWith(parPath);
}

function pathAllowed(p) {
    return _pathAllowed(p, conf.path);
}

async function getDir(p): Promise<any> {
    if (!pathAllowed(p)) return new Promise(res => res(null));
    p = path.join(conf.path, p);
    if (!fs.existsSync(p)) return new Promise(res => res(null));
    console.log(p);
    return new Promise(async res => {
        res(await Promise.all(fs.readdirSync(p, { withFileTypes: true, }).map(async f => {return { 
                name: f.name, 
                type: f.isDirectory() ? 'dir' : ((await ftype.fromFile(path.join(p, f.name)))||{mime: 'txt'}).mime, 
                ext: path.extname(f.name),
            };}))
        );
    });
}

function getHostInfo() {
    return {
        ip: ip.address(),
        username: os.userInfo().username,
        hostname: os.hostname(),
        uptime: os.uptime(),
        os: os.type(),
        platform: os.platform(),
    };
}

function stopServer(err: any) {
    if (err instanceof Error) {
        console.log(err.stack);
    }
    console.log(`[UKEY]: SIGTERM / Exception: Stopping server ... `);
    srv.close();
}

process.on('uncaughtException', stopServer);
process.on('SIGTERM', stopServer);