import axios from "axios";
import config from "./configParser.js";

const API_KEY = config.smsActivatorApiKey;
const FETCH_NUMBER_URL = `https://sms-activate.ru/stubs/handler_api.php?api_key=${API_KEY}&action=getNumber&service=go&operator=any&country=0`;

class SmsActivator {
  counstructor() {
    this.id = null;
    this.number = null;
    this.code = null;
  }

  getNumber() {
    return axios.get(FETCH_NUMBER_URL).then(response => {
      console.log(response.data);
      if (response.data.startsWith("ACCESS_NUMBER")) {
        const [_, id, number] = response.data.split(":");
        console.log(id);
        console.log(number);
        this.id = id;
        this.number = number;
      }
      return this.number;
    });
  }

  activateNumber() {
    axios.get(this.getActivationUrl()).then(response => {
      console.log(response.data);
    });
  }

  getCode() {
    return axios.get(this.getCodeUrl()).then(response => {
      console.log(response.data);
      if (response.data.startsWith("STATUS_OK")) {
        const [_, code] = response.data.split(":");
        console.log(code);
        this.code = code;
      }
      return this.code;
    });
  }

  getActivationUrl() {
    return `https://sms-activate.ru/stubs/handler_api.php?api_key=${API_KEY}&action=setStatus&status=1&id=${this.id}`;
  }

  getCodeUrl() {
    return `https://sms-activate.ru/stubs/handler_api.php?api_key=${API_KEY}&action=getStatus&id=${this.id}`;
  }
}

export default SmsActivator;
