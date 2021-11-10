import selenium from "selenium-webdriver";
import SmartGenerator from "./src/generator.js";
import SmsActivator from "./src/smsActivator.js";

const { Builder, By, Key, until } = selenium;
const START_URL =
    "https://accounts.google.com/signup/v2/webcreateaccount?service=mail&continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&flowName=GlifWebSignIn&flowEntry=SignUp";

(async function example() {
    const emailNumber = getNumberOfEmails();
    console.log(`Creating ${emailNumber} emails`);

    const driver = await new Builder().forBrowser("firefox").build();
    const gen = new SmartGenerator();
    const activator = new SmsActivator();

    gen.generate();
    console.log(gen);

    try {
        await driver.get(START_URL);
        await fillBasicInfo(driver, gen);

        // wait for phone number input
        await driver.wait(until.elementLocated(By.id("phoneNumberId")), 20000);
        await driver.sleep(3000);

        // wait for fetching phone number
        const number = await activator.getNumber();
        await activator.activateNumber();

        // fill phone number
        await driver
            .findElement(By.id("phoneNumberId"))
            .sendKeys(number, Key.ENTER);
        await driver.sleep(30000);

        // fetch code
        const code = await activator.getCode();
        await driver.wait(until.elementLocated(By.id("code")), 20000);
        await driver.sleep(3000);
        await driver.findElement(By.id("code")).sendKeys(code, Key.ENTER);

        // fill last step (birthday)
        await driver.sleep(3000);
        driver.executeScript(
            `document.getElementById('month').value = '${gen.monthOfBirth}'`
        );
        driver.executeScript(`document.getElementById('gender').value = '1'`);
        await driver.findElement(By.id("day")).sendKeys(gen.dayOfBirth);
        await driver
            .findElement(By.id("year"))
            .sendKeys(gen.yearOfBirth, Key.ENTER);
        await driver.sleep(3000);
        await driver.wait(
            until.elementLocated(By.xpath("//span[text() = 'Пропустить']")),
            20000
        );
        await driver.sleep(3000);
        driver.findElement(By.xpath("//span[text() = 'Пропустить']")).click();
        await driver.sleep(3000);
        await driver.wait(
            until.elementLocated(By.xpath("//span[text() = 'Принимаю']")),
            20000
        );
        await driver.sleep(3000);
        driver.findElement(By.xpath("//span[text() = 'Принимаю']")).click();
    } finally {
        await driver.quit();
    }
})();

async function fillBasicInfo(driver, gen) {
    await driver.findElement(By.name("firstName")).sendKeys(gen.firstName);
    await driver.findElement(By.name("lastName")).sendKeys(gen.lastName);
    await driver.findElement(By.name("Username")).sendKeys(gen.userName);
    await driver.findElement(By.name("Passwd")).sendKeys(gen.password);
    await driver
        .findElement(By.name("ConfirmPasswd"))
        .sendKeys(gen.password, Key.ENTER);
}

function getNumberOfEmails() {
    const args = process.argv;
    // search for key -n in arguments
    const numberArgKeyIdx = args.findIndex(arg => arg === "-n");
    // search for argument with number of emails (next to -n)
    const numberArgIdx = numberArgKeyIdx + 1;
    if (
        numberArgKeyIdx !== -1 &&
        args[numberArgIdx] &&
        args[numberArgIdx].match(/[0-9]+/)
    ) {
        return +args[numberArgIdx];
    }
    return 1;
}
