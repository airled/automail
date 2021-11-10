import fs from "fs";
import { resolve } from "path";

const config = JSON.parse(fs.readFileSync(resolve("config.json"), "utf8"));

export default config;
