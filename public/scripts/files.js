function pathJoin(d, p) {
    return (d + '/' + p).replace('//', '/');
}

function getDir() {
    return atob(window.location.href.replace(/https?:\/\//, '').split('/')[2]||'');
}

function setDir(dir) {
    window.history.pushState(null, '', `/files/${btoa(dir)}`);
}

async function loadDir() {
    return new Promise(resolve => {
        fetch(`/fs/${btoa(getDir())}`)
            .then(res => res.json())
            .then(res => {
                if (!res.success) window.location.assign('/files');
                resolve(res.dir);
            });
    });
}

function getFileIconClass(f) {
    if (f.type === 'dir') return 'far fa-folder';
    else if (f.type.startsWith('image/')) return 'far fa-image';
    else if (f.type.startsWith('video/')) return 'far fa-file-video';
    else if (f.type === 'application/pdf') return 'far fa-file-pdf';
    else if (f.type === 'application/zip') return 'far fa-file-archive';
    else if (f.type.startsWith('application/')) return 'fas fa-cogs';
    else {
        if (f.ext === '.txt') return 'far fa-file-alt';
        else if (f.ext === '.docx') return 'far fa-file-word';
        else if (f.ext === '.xlsx') return 'far fa-file-excel';
        else return 'far fa-file';
    }
}

function dispDir() {
    window.a.innerHTML = '';
    window.cuDir.forEach(f => {
        let d = document.createElement('div');
        d.classList.add('file');
        let c = document.createElement('div');
        let i = document.createElement('i');
        i.setAttribute('class', getFileIconClass(f));
        let s = document.createElement('span');
        s.innerHTML = f.name;
        c.appendChild(i);
        c.appendChild(s);
        d.appendChild(c);
        window.a.appendChild(d);
        if (f.type === 'dir') d.onclick = () => onDirClick(f.name);
        else d.onclick = () => onFileClick(f.name);
    });
}

async function onDirClick(dir) {
    window.a.innerHTML = '';
    setDir(pathJoin(getDir(), dir));
    window.cuDir = await loadDir();
    dispDir();
}

function onFileClick(f) {
    let a = document.createElement('a');
    a.download = f;
    a.href = `/f/${btoa(pathJoin(getDir(), f))}`;
    a.click();
}

window.onload = () => {
    window.a = document.getElementsByTagName('article')[0];
    dispDir();
};

window.onpopstate = async () => {
    window.a.innerHTML = '';
    window.cuDir = await loadDir();
    dispDir();
}