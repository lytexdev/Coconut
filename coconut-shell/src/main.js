import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";

import App from "./App.vue";
import Dashboard from "./components/Dashboard.vue";
import Login from "./components/Login.vue";
import Setup from "./components/setup/Setup.vue";

const app = createApp(App);

const routes = [
  { path: "/", name: "Dashboard", component: Dashboard },
  { path: "/login", name: "Login", component: Login },
  { path: "/setup", name: "Setup", component: Setup },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  fetch("/setup/status")
    .then((response) => response.json())
    .then((data) => {
      if (data.no_users && to.name !== "Setup") {
        next({ name: "Setup" });
      } else if (!data.no_users && to.name === "Setup" && !data.logged_in) {
        next({ name: "Login" });
      } else {
        next();
      }
    })
    .catch((error) => {
      console.error("Error checking users:", error);
      next();
    });
});

app.use(router);
app.mount("#app");
