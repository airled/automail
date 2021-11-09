import randomWords from "random-words";
import passwordGenerator from "generate-password";

const PASSWORD_OPTS = {
  length: 10,
  numbers: true,
  symbols: true,
  strict: true
};

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
    const [first, last] = randomWords(2);
    const randomNumber = Math.round(Math.random() * 2000000000);
    const userName = `${first}${last}${randomNumber}`;
    const password = passwordGenerator.generate(PASSWORD_OPTS);
    this.firstName = first;
    this.lastName = last;
    this.userName = userName;
    this.password = password;
  }
}

export default SmartGenerator;
