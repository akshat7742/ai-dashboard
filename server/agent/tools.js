export function getKPIAnalysis(data) {
  const summary = data.summary;

  return {
    sales: summary.sales,
    revenue: summary.revenue,
    orders: summary.orders,
    customers: summary.customers
  };
}


export function getTrendAnalysis(data) {
  const monthlySales = data.monthlySales;

  if (!monthlySales || monthlySales.length === 0) {
    return {
      message: "No monthly sales data available."
    };
  }

  const firstMonth = monthlySales[0];
  const lastMonth = monthlySales[monthlySales.length - 1];

  const change =
    ((lastMonth.sales - firstMonth.sales) / firstMonth.sales) * 100;

  const highestMonth = monthlySales.reduce((highest, current) => {
    return current.sales > highest.sales ? current : highest;
  });

  return {
    firstMonth: firstMonth,
    lastMonth: lastMonth,
    percentageChange: Number(change.toFixed(2)),
    highestMonth: highestMonth
  };
}


export function getRegionAnalysis(data) {
  const regions = data.regions;

  if (!regions || regions.length === 0) {
    return {
      message: "No region data available."
    };
  }

  const highestRegion = regions.reduce((highest, current) => {
    return current.sales > highest.sales ? current : highest;
  });

  const lowestRegion = regions.reduce((lowest, current) => {
    return current.sales < lowest.sales ? current : lowest;
  });

  return {
    highestRegion,
    lowestRegion,
    regions
  };
}