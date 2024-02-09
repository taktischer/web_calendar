const month = ["January","February","March","April","May","June","July","August","September","October","November","December"];
const currentDate = new Date();

let currentYear = currentDate.getFullYear();
let currentMonth = month[currentDate.getMonth()];
let currentMonth2 = currentDate.getMonth();
let currentDay = currentDate.getDate();

let offset = 0;
let offset2 = 0;

document.addEventListener("DOMContentLoaded", function() {
    const currentDate = new Date();
    let currentYear = currentDate.getFullYear();
    let currentMonth = month[currentDate.getMonth()];
    let currentMonth2 = currentDate.getMonth();
    let offset = 0;
    let offset2 = 0;

    updateCalendar(currentYear, currentMonth2);
    document.getElementById("month").innerHTML = '<div class="change-month-button-container">' + '<button class="change-month-button button" onclick="ChangeOffsetNegative()"><</button>' + '</div>' + '<div class="change-month-button-conatainer">' + currentMonth + " " + currentYear + '</div>' + '<div class="change-month-button-container">' + '<button class="change-month-button button" onclick="ChangeOffsetPositive()">></button>' + '</div>';
    let calendar_container = document.getElementById("calendar");
    let calendar_container_height = calendar_container.clientHeight;
    let sidenavbar_container = document.getElementById("sidenavbar");
    sidenavbar_container.style.height = calendar_container_height + "px";
});

function ChangeOffsetNegative() {
    offset -= 1;
    if (offset < 0){
        offset = 0;
    }
    if (currentMonth === "January") {
        offset2 -= 1;
        currentYear = currentDate.getFullYear()+offset2;
        offset = 11;
    }
    currentMonth = month[offset];
    currentMonth2 = offset;
    updateCalendar(currentYear, currentMonth2);
    document.getElementById("month").innerHTML = '<div class="change-month-button-container">' + '<button class="change-month-button button" onclick="ChangeOffsetNegative()"><</button>' + '</div>' + '<div class="change-month-button-conatainer">' + currentMonth + " " + currentYear + '</div>' + '<div class="change-month-button-container">' + '<button class="change-month-button button" onclick="ChangeOffsetPositive()">></button>' + '</div>';
    let calendar_container = document.getElementById("calendar");
    let calendar_container_height = calendar_container.clientHeight;
    let sidenavbar_container = document.getElementById("sidenavbar");
    sidenavbar_container.style.height = calendar_container_height + "px";
}

function ChangeOffsetPositive() {
    offset += 1;

    if (offset > 11){
        offset = 11;
    }

    if (currentMonth === "December") {
        offset2 += 1;
        currentYear = currentDate.getFullYear()+offset2;
        offset = 0;
    }
    currentMonth = month[offset];
    currentMonth2 = offset;
    updateCalendar(currentYear, currentMonth2);
    document.getElementById("month").innerHTML = '<div class="change-month-button-container">' + '<button class="change-month-button button" onclick="ChangeOffsetNegative()"><</button>' + '</div>' + '<div class="change-month-button-conatainer">' + currentMonth + " " + currentYear + '</div>' + '<div class="change-month-button-container">' + '<button class="change-month-button button" onclick="ChangeOffsetPositive()">></button>' + '</div>';
    let calendar_container = document.getElementById("calendar");
    let calendar_container_height = calendar_container.clientHeight;
    let sidenavbar_container = document.getElementById("sidenavbar");
    sidenavbar_container.style.height = calendar_container_height + "px";
    console.log(calendar_container_height);
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
        <button id="${i}" class="calendar-day-button button" onclick="ShowAppointment(${i}, currentMonth2, currentYear)">${i}</button>
        `;
    }
    for (let i = modulo; i < 6; i++) {
        const wocheDiv = document.getElementById(`calendar-week-${woche}`);
        wocheDiv.innerHTML += `
        <button class="calendar-day-button button"></button>
        `;
    }
}

function getDaysInMonth(year, month) {
    const lastDay = new Date(year, month + 1, 0).getDate();
    return lastDay;
}

function redirectAppointments(day, month, year) {
    let currentURL = "http://127.0.0.1:8000";
    let updatedURL = currentURL + "/" + day + "/" + month + "/" + year;
    window.location.href = updatedURL;
}