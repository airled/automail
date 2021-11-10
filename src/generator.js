import randomWords from "random-words";
import passwordGenerator from "generate-password";

const PASSWORD_OPTS = {
  length: 10,
  numbers: true,
  symbols: true,
  strict: true
};

const DAYS = [...Array(28).keys()].map(x => (x + 1).toString());
const MONTHS = [...Array(12).keys()].map(x => (x + 1).toString());
const YEARS = [...Array(30).keys()].map(x => (x + 1980).toString());

class SmartGenerator {
  constructor() {
    this.firstName = "";
    this.lastName = "";
    this.userName = "";
    this.password = "";
    this.dayOfBirth = "";
    this.monthOfBirth = "";
    this.yearOfBirth = "";
  }

  generate() {
    const [first, last, third] = randomWords(3);
    const randomNumber = Math.round(Math.random() * 2000);
    const userName = `${first}${last}${third}${randomNumber}`;
    const password = passwordGenerator.generate(PASSWORD_OPTS);
    this.firstName = first;
    this.lastName = last;
    this.userName = userName;
    this.password = password;
    this.dayOfBirth = this.getSample(DAYS);
    this.monthOfBirth = this.getSample(MONTHS);
    this.yearOfBirth = this.getSample(YEARS);
  }

  getSample(ary) {
    return ary[Math.floor(Math.random() * ary.length)];
  }
}

export default SmartGenerator;
