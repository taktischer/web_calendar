const months = ["January","February","March","April","May","June","July","August","September","October","November","December"];
const currentDate = new Date();
let day, month, year;

document.addEventListener("DOMContentLoaded", function() {
    let split_url = new URL(window.location.href).toString().split("/");
    try {
        if (split_url.length === 7) {
            day = parseInt(split_url[3])
            month = parseInt(split_url[4])
            year = parseInt(split_url[5])
        } else {
            throw Error;
        }
    } catch (e) {
        let today = new Date()
        day = parseInt(today.getDay());
        month = parseInt(today.getMonth());
        year = parseInt(today.getFullYear());
    }

    updateCalendar(year, month);
    document.getElementById("month").innerHTML = '<div class="change-month-button-container">' +
        '<button class="change-month-button button" onclick="ChangeOffsetNegative()"><</button>'
        + '</div>' + '<div class="change-month-button-conatainer">' + months[month-1] + " " + year +
        '</div>' + '<div class="change-month-button-container">' +
        '<button class="change-month-button button" onclick="ChangeOffsetPositive()">></button>' + '</div>';
});

function ChangeOffsetNegative() {
    if (month == 1) {
        year -= 1;
        month = 12
        let daysInMonth = getDaysInMonth(year, month)
        if (day > daysInMonth) {
            day = daysInMonth;
        }
    } else {
        month -= 1;
        let daysInMonth = getDaysInMonth(year, month)
        if (day > daysInMonth) {
            day = daysInMonth;
        }
    }
    location.href = "http://127.0.0.1:8000" + "/" + day + "/" + month + "/" + year;
}

function ChangeOffsetPositive() {
    if (month == 12) {
        year += 1;
        month = 1;
    } else {
        month += 1
    }

    let daysInMonth = getDaysInMonth(year, month);
    if (day > daysInMonth) {
        day = daysInMonth;
    }

    location.href = "http://127.0.0.1:8000" + "/" + day + "/" + month + "/" + year;
}

function updateCalendar(year, month) {
    const calendarMain = document.getElementById("calendar-main");
    calendarMain.innerHTML = ``;
    calendarMain.innerHTML = `
    <div class="calendar-week" id="calendar-week-0"></div>
    `;
    let woche = 0;
    let firstDay = (new Date(year, month)).getDay();
    let placeholder = firstDay === 0 ? 6 : firstDay - 1;
    for (let i = 0; i < placeholder; i++) {
        const wocheDiv = document.getElementById(`calendar-week-${woche}`);
        wocheDiv.innerHTML += `
        <button class="calendar-day-button button"></button>
        `;
    }
    let j = placeholder;
    let modulo = 0;
    console.log(month)
    const daysInMonth = getDaysInMonth(year, month);
    for (let i = 1; i <= daysInMonth; i++) {
        modulo = j % 7;
        if (modulo === 0) {
            woche++;
            calendarMain.innerHTML += `
                <div class="calendar-week" id="calendar-week-${woche}"></div>
            `;
        }
        j = j + 1;
        const wocheDiv = document.getElementById(`calendar-week-${woche}`);
        wocheDiv.innerHTML += `
        <button id="${i}" class="calendar-day-button button" onclick="ShowAppointment(${i}, month, year)">${i}</button>
        `;
    }
    for (let i = modulo; i < 6; i++) {
        const wocheDiv = document.getElementById(`calendar-week-${woche}`);
        wocheDiv.innerHTML += `
        <button class="calendar-day-button button"></button>
        `;
    }

    if (!window.location.href.endsWith("http://127.0.0.1:8000") && !window.location.href.endsWith("http://127.0.0.1:8000/")) {
        let urlparts = window.location.href;
        let urlsplit = urlparts.split("/");
        document.getElementById(`${urlsplit[3]}`).classList.add("highlighted");
    }
}

function getDaysInMonth(year, month) {
    const lastDay = new Date(year, month, 0).getDate();
    return lastDay;
}

function redirectAppointments(day, month, year) {
    let currentURL = "http://127.0.0.1:8000";
    let updatedURL = currentURL + "/" + day + "/" + month + "/" + year;
    window.location.href = updatedURL;
}