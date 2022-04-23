import { extend, localize } from "vee-validate";
import { required, email, min } from "vee-validate/dist/rules";

const dictionary = {
    en: {
        messages: {
            required: () => '* Required',
        },
    },
};

// Install required rule.
extend("required", required);

// Install email rule.
extend("email", email);

// Install min rule.
extend("min", min);

localize(dictionary);