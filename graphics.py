import plotly.graph_objs as go
import plotly.io as pio
import pandas as pd
import os
from PyQt6.QtCore import QUrl

class Graphics:
    def __init__(self, cursor, browser):
        self.cursor = cursor
        self.browser = browser

    def create_graphic(self, selected_dates, selected_trading_dates, options, table_name, paper_name, put_or_call):
        fig = go.Figure()
        
        if options == "Vol/Strike Graph":
            self._create_vol_strike_graph(fig, selected_dates, selected_trading_dates, table_name, paper_name, put_or_call)
        else:  # "OI/Strike Graph"
            self._create_oi_strike_graph(fig, selected_dates, selected_trading_dates, table_name, paper_name, put_or_call)

        graph_html = pio.to_html(fig, full_html=False)
        self._save_and_show_graph(graph_html)

    def _create_vol_strike_graph(self, fig, selected_dates, selected_trading_dates, table_name, paper_name, put_or_call):
        if put_or_call in ("put", "call"):
            query = f"SELECT strike, implied_volatility, expiration, date FROM {table_name} WHERE type = '{put_or_call}' AND symbol = '{paper_name}' ORDER BY (strike * 1.00)"
        else:
            query = f"SELECT strike, implied_volatility, expiration, date, type FROM {table_name} WHERE symbol = '{paper_name}' ORDER BY (strike * 1.00)"

        all_data = pd.DataFrame(self.cursor.execute(query).fetchall(), columns=["strike", "implied_volatility", "expiration", "trading_data"])
        
        for selected_date in selected_dates:
            for trading_date in selected_trading_dates:
                trace = go.Scatter(
                    x=all_data[(all_data["expiration"] == selected_date) & (all_data["trading_data"] == trading_date)]["strike"],
                    y=all_data[(all_data["expiration"] == selected_date) & (all_data["trading_data"] == trading_date)]["implied_volatility"],
                    mode='lines+markers',
                    name=f"{selected_date} | {trading_date}"
                )
                fig.add_trace(trace)

        fig.update_layout(title=f"Graph for {paper_name}", xaxis_title="Strike", yaxis_title="Volatility")

    def _create_oi_strike_graph(self, fig, selected_dates, selected_trading_dates, table_name, paper_name, put_or_call):
        if put_or_call in ("put", "call"):
            query = f"SELECT strike, open_interest, expiration, date FROM {table_name} WHERE type = '{put_or_call}' AND symbol = '{paper_name}' ORDER BY (strike * 1.00)"
        else:
            query = f"SELECT strike, open_interest, expiration, date FROM {table_name} WHERE symbol = '{paper_name}' ORDER BY (strike * 1.00)"

        all_data = pd.DataFrame(self.cursor.execute(query).fetchall(), columns=["strike", "open_interest", "expiration", "trading_data"])

        for selected_date in selected_dates:
            for trading_date in selected_trading_dates:
                trace = go.Bar(
                    x=all_data[(all_data["expiration"] == selected_date) & (all_data["trading_data"] == trading_date)]["strike"],
                    y=all_data[(all_data["expiration"] == selected_date) & (all_data["trading_data"] == trading_date)]["open_interest"],
                    name=f"{selected_date} | {trading_date}",
                    marker_color='blue' if put_or_call == "put" else 'red'
                )
                fig.add_trace(trace)

        fig.update_layout(title=f"Graph for {paper_name}", xaxis_title="Strike", yaxis_title="Open Interest")

    def _save_and_show_graph(self, graph_html):
        file_path = "graph.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(graph_html)
        self.browser.setUrl(QUrl.fromLocalFile(os.path.abspath(file_path)))