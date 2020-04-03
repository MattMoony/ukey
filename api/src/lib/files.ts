import fs from 'fs';
import path from 'path';
import ftype from 'file-type';

export function pathAllowed(p, basePath) {
    return path.join(basePath, p).startsWith(basePath);
}

export function getDir(p, basePath): Promise<any> {
    if (!pathAllowed(p, basePath)) return new Promise(res => res(null));
    p = path.join(basePath, p);
    if (!(fs.existsSync(p) && fs.lstatSync(p).isDirectory())) return new Promise(res => res(null));
    console.log('fs: ' + p);
    return new Promise(async res => {
        res(await Promise.all(fs.readdirSync(p, { withFileTypes: true, }).map(async f => {return {
            name: f.name,
            type: f.isDirectory() ? 'dir' : ((await ftype.fromFile(path.join(p, f.name)))||{mime: 'txt'}).mime,
            ext: path.extname(f.name),
        }})));
    });
}