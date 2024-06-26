import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "./index.css";
import "leaflet/dist/leaflet.css";
import "vue-map-ui/dist/normalize.css";
import "vue-map-ui/dist/style.css";
import "vue-map-ui/dist/theme-all.css";

createApp(App)
  .use(store)
  .use(router)
  .mount("#app");
