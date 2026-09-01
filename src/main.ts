import { createApp } from "vue";
import { createPinia } from "pinia";

import App from "./App.vue";
import router from "./router";

import ECharts from "vue-echarts";

import { use } from "echarts/core";

import {
  CanvasRenderer
} from "echarts/renderers";

import {
  BarChart,
  LineChart
} from "echarts/charts";

import {
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent
} from "echarts/components";

use([
  CanvasRenderer,
  BarChart,
  LineChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
]);

const app = createApp(App);

app.component("v-chart", ECharts);

app.use(createPinia());
app.use(router);

app.mount("#app");