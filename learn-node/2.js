const os = require("os");
console.log("Operating System:", os.type());
console.log("CPU Architecture:", os.arch());
console.log("Total Memory:", os.totalmem());
console.log("Free Memory:", os.freemem());

const d = new Date();
console.log("Current Date and Time:", d.toString());
console.log("Current Year:", d.getFullYear());
console.log("Current Month:", d.getMonth() + 1);
