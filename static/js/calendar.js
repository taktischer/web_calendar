const month = ["January","February","March","April","May","June","July","August","September","October","November","December"];
const currentDate = new Date();

let currentYear = currentDate.getFullYear();
let currentMonth = month[currentDate.getMonth()];
let currentMonth2 = currentDate.getMonth();
let currentDay = currentDate.getDate();

let offset = 0;
let offset2 = 0;

function ChangeOffsetNegative() {
    offset -= 1;
    if (currentMonth === "January") {
        offset2 -= 1;
        if (offset2 === 0) {
            offset2 -= 1;
        }
        currentYear = currentDate.getFullYear()+offset2;
    }
    currentMonth = month[currentDate.getMonth()+offset];
    currentMonth2 = currentDate.getMonth()+offset;
    document.getElementById("month").innerHTML = '<button class="change-month-button button" onclick="ChangeOffsetNegative()">Negative</button>' + " " + currentMonth + " " + currentYear + " " + '<button class="change-month-button button" onclick="ChangeOffsetPositive()">Positive</button>';
}
function ChangeOffsetPositive() {
    offset += 1;
    if (currentMonth === "December") {
        offset2 += 1;
        if (offset2 === 0) {
            offset2 += 1;
        }
        currentYear = currentDate.getFullYear()+offset2;
    }
    currentMonth = month[currentDate.getMonth()+offset];
    currentMonth2 = currentDate.getMonth()+offset;
    document.getElementById("month").innerHTML = '<button class="change-month-button button" onclick="ChangeOffsetNegative()">Negative</button>' + " " + currentMonth + " " + currentYear + " " + '<button class="change-month-button button" onclick="ChangeOffsetPositive()">Positive</button>';
}

document.getElementById("month").innerHTML = '<button class="change-month-button button" onclick="ChangeOffsetNegative()">Negative</button>' + " " + currentMonth + " " + currentYear + " " + '<button class="change-month-button button" onclick="ChangeOffsetPositive()">Positive</button>';

let firstDay = (new Date(currentDate.getFullYear(), currentDate.getMonth())).getDay();

function getDaysInMonth(year, month) {
    const lastDay = new Date(year, month + 1, 0).getDate();
    return lastDay;
}

const daysInCurrentMonth = getDaysInMonth(currentYear, currentMonth2);

calendarMain = document.getElementById("calendar-main");
calendarMain.innerHTML = ``;
calendarMain.innerHTML = `
<div class="calendar-week" id="calendar-week-0"></div>
`;

let woche = 0

for (let i = 1; i < firstDay; i++) {
    wocheDiv = document.getElementById(`calendar-week-${woche}`);
    wocheDiv.innerHTML += `
    <button class="calendar-day-button button"></button>
    `;
}
let j = firstDay-1;
let modulo = 0;
for (let i = 1; i <= daysInCurrentMonth; i++) {
    modulo = j % 7;
    if (modulo === 0) {
        woche++;
        calendarMain.innerHTML += `
            <div class="calendar-week" id="calendar-week-${woche}"></div>
        `;
    }
    j = j + 1;
    wocheDiv = document.getElementById(`calendar-week-${woche}`);
    wocheDiv.innerHTML += `
    <button class="calendar-day-button button" onclick="ShowAppointment()">${i}</button>
    `;
}

for (let i = modulo; i < 6; i++) {
    wocheDiv = document.getElementById(`calendar-week-${woche}`);
    wocheDiv.innerHTML += `
    <button class="calendar-day-button button"></button>
    `;
}