// const os = require("os");
import os from "os";
// bycript is a library for hashing passwords
// const bcrypt = require("bcrypt");
import bcrypt from "bcrypt";

const d = bcrypt.hash("mysecretpassword", 10);
console.log(
  d.then((hash) => {
    console.log("Hashed Password:", hash);
  }),
);

// console.log("Operating System:", os.type());

import { type, arch } from "os";

console.log("Operating System:", type());
console.log("CPU Architecture:", arch());
// console.log("Total Memory:", os.totalmem());
// console.log("Free Memory:", os.freemem());
