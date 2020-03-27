const BUFF_SIZE = 25;

const COLORS = [ '#BA1E1E', '#BA6C1E', '#BABA1E', '#1EBA1E', '#1EBA6C', '#1EBABA', '#1E6CBA', '#1E1EBA', '#6C1EBA', '#BA1EBA', '#BA1E6C', '#CA2075' ];
const cpuResConf = baseConf('CPU-Usage'),
      ramResConf = baseConf('RAM-Usage');

function initGraph(res) {
    window.cpuCtx = document.getElementById('cpu-can');
    window.ramCtx = document.getElementById('ram-can');
    cpuResConf.data.datasets = [];
    ramResConf.data.datasets = [];
    res.cpuUsage.forEach((c,i) => {
        cpuResConf.data.datasets.push({
            label: `CPU-${i}`,
            data: [ Math.round(c*10000)/100 ],
            fill: false,
            backgroundColor: COLORS[i%COLORS.length],
            borderColor: COLORS[i%COLORS.length],
        });
    });
    ramResConf.data.datasets.push({
        label: `RAM`,
        data: [ Math.round(res.ramUsage*10000)/100 ],
        fill: true,
        backgroundColor: 'rgba(189, 41, 41, .1)',
        borderColor: '#BD2929',
    });
    window.cpuUsage = new Chart(window.cpuCtx, cpuResConf);
    window.ramUsage = new Chart(window.ramCtx, ramResConf);
}

function updateGraph(res) {
    res.cpuUsage.forEach((c,i) => {
        cpuResConf.data.datasets[i].data.push(Math.round(c*10000)/100);
        cpuResConf.data.datasets[i].data = cpuResConf.data.datasets[i].data.slice(-BUFF_SIZE);
    });
    window.cpuUsage.update(0);
    ramResConf.data.datasets[0].data.push(Math.round(res.ramUsage*10000)/100);
    ramResConf.data.datasets[0].data = ramResConf.data.datasets[0].data.slice(-BUFF_SIZE);
    window.ramUsage.update(0);
}

function baseConf(title) {
    return {
        type: 'line',
        data: {
            labels: new Array(BUFF_SIZE).fill(null).map((_,i) => -BUFF_SIZE+i),
        },
        options: {
            responsive: false,
            title: {
                display: true,
                text: title,
            },
            tooltips: {
                mode: 'index',
                intersect: false,
            },
            hover: {
                mode: 'nearest',
                intersect: true,
            },
            scales: {
                xAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Time [s]',
                    },
                }],
                yAxes: [{
                    display: true,
                    scaleLabel: {
                        display: true,
                        labelString: 'Usage [%]',
                    },
                    ticks: {
                        suggestedMin: 0,
                        suggestedMax: 100,
                        beginAtZero: true,
                    }
                }],
            }
        },
    };
}

const sock = io();
sock.on('resources', res => {
    if (!cpuResConf.data.datasets) initGraph(res);
    else updateGraph(res);
});