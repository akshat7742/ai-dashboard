import { defineStore } from "pinia";
import api from "../services/api";

export const useDashboardStore = defineStore("dashboard", {
  state: () => ({
    dashboard: null as any,
    loading: false,
  }),

  getters: {
    summary: (state) => state.dashboard?.summary,
    monthlySales: (state) => state.dashboard?.monthlySales || [],
    regions: (state) => state.dashboard?.regions || [],
  },

  actions: {
    async loadDashboard() {
      this.loading = true;

      try {
        const response = await api.get("/dashboard");
        this.dashboard = response.data;
      } catch (error) {
        console.error(error);
      } finally {
        this.loading = false;
      }
    },
  },
});