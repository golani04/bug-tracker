const type = ['primary', 'info', 'success', 'warning', 'danger'];

const demo = {
    initPickColor: function () {
        $('.pick-class-label').click(function () {
            var new_class = $(this).attr('new-class');
            var old_class = $('#display-buttons').attr('data-class');
            var display_div = $('#display-buttons');
            if (display_div.length) {
                var display_buttons = display_div.find('.btn');
                display_buttons.removeClass(old_class);
                display_buttons.addClass(new_class);
                display_div.attr('data-class', new_class);
            }
        });
    },


    initDashboardPageCharts: function () {

        const chartPreferences = document.querySelector('#chartPreferences');
        if (!chartPreferences) return;

        var dataPreferences = {
            series: [
                [25, 30, 20, 25]
            ]
        };

        var optionsPreferences = {
            donut: true,
            donutWidth: 40,
            startAngle: 0,
            total: 100,
            showLabel: false,
            axisX: {
                showGrid: false
            }
        };

        Chartist.Pie('#chartPreferences', dataPreferences, optionsPreferences);

        Chartist.Pie('#chartPreferences', {
            labels: ['53%', '36%', '11%'],
            series: [53, 36, 11]
        });
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
