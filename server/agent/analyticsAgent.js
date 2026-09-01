import {
  getKPIAnalysis,
  getTrendAnalysis,
  getRegionAnalysis
} from "./tools.js";

import { analyzeDashboard } from "../ai.js";


export async function runAnalyticsAgent(question, dashboardData) {

  const lowerQuestion = question.toLowerCase();

  let analysis = {};

  /*
   * Decide which analytical tools are required
   */

  if (
    lowerQuestion.includes("kpi") ||
    lowerQuestion.includes("revenue") ||
    lowerQuestion.includes("sales") ||
    lowerQuestion.includes("orders") ||
    lowerQuestion.includes("customers")
  ) {
    analysis.kpi = getKPIAnalysis(dashboardData);
  }


  if (
    lowerQuestion.includes("trend") ||
    lowerQuestion.includes("increase") ||
    lowerQuestion.includes("decrease") ||
    lowerQuestion.includes("growth") ||
    lowerQuestion.includes("month")
  ) {
    analysis.trend = getTrendAnalysis(dashboardData);
  }


  if (
    lowerQuestion.includes("region") ||
    lowerQuestion.includes("north") ||
    lowerQuestion.includes("south") ||
    lowerQuestion.includes("east") ||
    lowerQuestion.includes("west")
  ) {
    analysis.region = getRegionAnalysis(dashboardData);
  }


  /*
   * If no specific tool was selected,
   * provide all available analysis.
   */

  if (Object.keys(analysis).length === 0) {

    analysis = {
      kpi: getKPIAnalysis(dashboardData),
      trend: getTrendAnalysis(dashboardData),
      region: getRegionAnalysis(dashboardData)
    };

  }


  /*
   * Send the calculated analysis to the LLM
   */

  const enrichedData = {
    originalQuestion: question,
    analysis
  };


  return await analyzeDashboard(
    question,
    enrichedData
  );
}