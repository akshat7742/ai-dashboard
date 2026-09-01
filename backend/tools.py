from langchain_core.tools import tool


def create_analytics_tools(dashboard_data):

    @tool
    def get_dashboard_summary() -> dict:
        """
        Get a complete high-level summary of the dashboard.
        Use this when the user asks for an overall dashboard
        summary, key insights, main issues, or recommendations.
        """

        summary = dashboard_data.get(
            "summary",
            {}
        )

        monthly_sales = dashboard_data.get(
            "monthlySales",
            []
        )

        regions = dashboard_data.get(
            "regions",
            []
        )

        highest_month = None
        lowest_month = None

        if monthly_sales:
            highest_month = max(
                monthly_sales,
                key=lambda item: item.get("sales", 0)
            )

            lowest_month = min(
                monthly_sales,
                key=lambda item: item.get("sales", 0)
            )

        highest_region = None
        lowest_region = None

        if regions:
            highest_region = max(
                regions,
                key=lambda item: item.get("sales", 0)
            )

            lowest_region = min(
                regions,
                key=lambda item: item.get("sales", 0)
            )

        return {
            "kpis": summary,
            "highest_month": highest_month,
            "lowest_month": lowest_month,
            "highest_region": highest_region,
            "lowest_region": lowest_region
        }
    
    @tool
    def get_kpi_analysis() -> dict:
        """
        Get dashboard KPIs including sales,
        revenue, orders, and customers.
        """

        summary = dashboard_data.get(
            "summary",
            {}
        )

        return {
            "sales": summary.get("sales", 0),
            "revenue": summary.get("revenue", 0),
            "orders": summary.get("orders", 0),
            "customers": summary.get("customers", 0)
        }


    @tool
    def get_trend_analysis() -> dict:
        """
        Analyze monthly sales trends,
        percentage growth and highest month.
        """

        monthly_sales = dashboard_data.get(
            "monthlySales",
            []
        )

        if not monthly_sales:
            return {
                "message":
                "No monthly sales data available."
            }

        first_month = monthly_sales[0]

        last_month = monthly_sales[-1]

        first_sales = first_month.get(
            "sales",
            0
        )

        last_sales = last_month.get(
            "sales",
            0
        )

        if first_sales == 0:

            percentage_change = 0

        else:

            percentage_change = (
                (last_sales - first_sales)
                / first_sales
            ) * 100


        highest_month = max(
            monthly_sales,
            key=lambda item:
            item.get("sales", 0)
        )


        return {

            "first_month":
                first_month,

            "last_month":
                last_month,

            "percentage_change":
                round(
                    percentage_change,
                    2
                ),

            "highest_month":
                highest_month
        }


    @tool
    def get_region_analysis() -> dict:
        """
        Analyze sales performance by region.
        """

        regions = dashboard_data.get(
            "regions",
            []
        )

        if not regions:

            return {
                "message":
                "No region data available."
            }


        highest_region = max(
            regions,
            key=lambda item:
            item.get("sales", 0)
        )


        lowest_region = min(
            regions,
            key=lambda item:
            item.get("sales", 0)
        )


        return {

            "highest_region":
                highest_region,

            "lowest_region":
                lowest_region,

            "regions":
                regions
        }


    return [
        get_dashboard_summary,
        get_kpi_analysis,
        get_trend_analysis,
        get_region_analysis
    ]