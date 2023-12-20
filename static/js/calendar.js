const month = ["January","February","March","April","May","June","July","August","September","October","November","December"];
const currentDate = new Date();

const currentYear = currentDate.getFullYear();
let currentMonth = month[currentDate.getMonth()];
let currentMonth2 = currentDate.getMonth();
let currentDay = currentDate.getDate();

document.getElementById("month").innerHTML = currentMonth + " " + currentYear;

let firstDay = (new Date(currentDate.getFullYear(), currentDate.getMonth())).getDay();
console.log(firstDay)

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
for (let i = 1; i <= daysInCurrentMonth; i++) {
    let modulo = j % 7;
    if (modulo == 0) {
        woche++;
        calendarMain.innerHTML += `
            <div class="calendar-week" id="calendar-week-${woche}"></div>
        `;
    }
    j = j + 1;
    wocheDiv = document.getElementById(`calendar-week-${woche}`);
    wocheDiv.innerHTML += `
    <button class="calendar-day-button button">${i}</button>
    `;
}