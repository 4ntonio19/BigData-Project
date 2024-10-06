import os
import sys

import dash

sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             '../')))

from linkedin_dashboard.layout.dashboard_layout import layout

from project.linkedin_dashboard.callbacks.charts import create_callbacks
from project.linkedin_dashboard.process.process_data import \
    process_job_postings
from project.linkedin_dashboard.settings.settings import get_settings

app = dash.Dash(__name__)
process_job_postings()
create_callbacks(app)
settings = get_settings()
app.layout = layout

if __name__ == '__main__':
    app.run_server(
        debug=True if settings.env_settings.environment == 'DEV' else False)
