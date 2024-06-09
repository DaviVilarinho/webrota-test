/* eslint-disable */
// vee validate não tem tipos...
import {
  configure,
  defineRule,
  ErrorMessage as VeeErrorMessage,
  Field as VeeField,
  Form as VeeForm,
} from "vee-validate";
import {
  alpha_spaces as alphaSpaces,
  between,
  confirmed,
  email,
  max,
  min,
  not_one_of as excluded,
  numeric,
  required,
} from "@vee-validate/rules";

export default {
  install(app) {
    app.component("VeeForm", VeeForm);
    app.component("VeeField", VeeField);
    app.component("VeeErrorMessage", VeeErrorMessage);

    defineRule("required", required);
    defineRule("min", min);
    defineRule("max", max);
    defineRule("alpha_spaces", alphaSpaces);

    configure({
      generateMessage: (context) => {
        const messages = {
          required: `O campo ${context.field} é obrigatório.`,
          min: `O campo ${context.field} é menor que o esperado.`,
          max: `O campo ${context.field} é maior que o esperado.`,
          alpha_spaces:
            `O campo ${context.field} só aceita caracteres alfanuméricos e espaço.`,
        };

        return messages[context.rule.name] ??
          `O campo ${context.field} não é válido.`;
      },
      validateOnBlur: true,
      validateOnChange: true,
      validateOnInput: false,
      validateOnModelUpdate: true,
    });
  },
};
