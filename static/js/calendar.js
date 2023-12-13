const month = ["January","February","March","April","May","June","July","August","September","October","November","December"];

const currentDate = new Date();
let currentMonth = month[currentDate.getMonth()];
document.getElementById("month").innerHTML = currentMonth;