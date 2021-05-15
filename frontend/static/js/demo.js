const type = ['primary', 'info', 'success', 'warning', 'danger'];

const demo = {
    initDashboardPageCharts: async () => {
        const chartPreferences = document.querySelector('#chart-issues');
        if (!chartPreferences) return;

        const [issues, details] = await Promise.all([fetch('/api/v1/issues').then(response => response.json()), fetch('/api/v1/issues/details').then(response => response.json())]);
        console.log(issues);
        console.log(details);
        // severity
        const severityColors = ['text-info', 'text-warning', 'text-danger'];
        const data = { 'labels': [], 'series': [] };
        const counter = {};

        for (let issue of issues) {
            // count number of issues by severity
            counter[issue.severity] = counter[issue.severity] ? counter[issue.severity] + 1 : 1;
        }


        for (let key in counter) {
            data['series'][key] = parseInt(counter[key] / issues.length * 100);
            data['labels'][key] = `${data['series'][key]}%`;
        }

        console.log(counter);
        console.log(data);

        Chartist.Pie('#chart-issues', data);
    },

    showNotification: function (from, align) {
        let color = Math.floor((Math.random() * 4) + 1);

        $.notify({
            icon: "nc-icon nc-app",
            message: "Welcome to <b>Light Bootstrap Dashboard</b> - a beautiful freebie for every web developer."

        }, {
            type: type[color],
            timer: 8000,
            placement: {
                from: from,
                align: align
            }
        });
    }
}

// open/close modals for issues
const clearClearForm = (elem) => {
    if (!elem) return;

    elem.addEventListener("show.bs.modal", (e) => {
        if (!e.relatedTarget) return;

        const form = elem.querySelector('#create-issue-form');
        const elements = new Set(['id', 'title', 'description', 'due', 'severity', 'status', 'label']);

        for (let item of form) {
            if (elements.has(item.name)) {
                if (item.nodeName == 'SELECT') {
                    item.options[item.selectedIndex].removeAttribute('selected');
                } else {
                    item.value = '';
                }
            }
        }
    });
}


const showIssueModal = (createEl, delEl) => {
    const location = window.location;
    const hasItemId = location.href.includes('item_id');
    const hasDeleted = location.href.includes('deleted');

    if (location.pathname.includes('issue')) {
        if (createEl && hasItemId && !hasDeleted) {
            new bootstrap.Modal(createEl).show();
        }
        if (delEl && hasItemId && hasDeleted) {
            new bootstrap.Modal(delEl).show();
        }
    }
}

const createIssueModal = document.querySelector('#create-issue-modal');
const deleteIssueModal = document.querySelector('#delete-issue-modal');


clearClearForm(createIssueModal);
showIssueModal(createIssueModal, deleteIssueModal);
