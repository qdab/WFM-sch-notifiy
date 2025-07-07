import csv
import os
from datetime import datetime, timedelta
from urllib.request import urlopen
from wsgiref.simple_server import make_server

# Number of days ahead to display on the web page
DAYS_AHEAD = int(os.environ.get("DAYS_AHEAD", "7"))
# Optional port configuration for the server
SERVER_PORT = int(os.environ.get("PORT", "8000"))

SCHEDULE_FILE = os.environ.get('SCHEDULE_FILE', 'schedule.csv')
SCHEDULE_URL = os.environ.get('SCHEDULE_URL')

def load_schedule(path=SCHEDULE_FILE):
    """Return list of schedule entries as dicts with date objects."""
    entries = []
    try:
        if SCHEDULE_URL:
            stream = urlopen(SCHEDULE_URL)
        else:
            stream = open(path, 'rb')
        with stream as raw:
            reader = csv.reader(line.decode('utf-8') for line in raw)
            next(reader, None)  # drop header
            for row in reader:
                if len(row) >= 2:
                    try:
                        d = datetime.strptime(row[0], "%Y-%m-%d").date()
                    except ValueError:
                        continue
                    entries.append({'date': d, 'task': row[1]})
    except FileNotFoundError:
        pass
    except Exception:
        pass
    return entries


def get_upcoming_entries(entries, days=7, start=None):
    """Return entries within the next ``days`` starting from ``start``."""
    start = start or datetime.today().date()
    end = start + timedelta(days=days)
    upcoming = []
    for e in entries:
        if start <= e['date'] <= end:
            upcoming.append(e)
    return upcoming


def render_table(entries):
    rows = '\n'.join(
        f'<tr><td>{e["date"].isoformat()}</td><td>{e["task"]}</td></tr>'
        for e in entries
    )
    return f"""<html><body>
<h1>Upcoming Schedule</h1>
<table border='1'>
<tr><th>Date</th><th>Task</th></tr>
{rows}
</table>
</body></html>"""


def application(environ, start_response):
    entries = load_schedule()
    upcoming = get_upcoming_entries(entries, days=DAYS_AHEAD)
    content = render_table(upcoming)
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    return [content.encode('utf-8')]


def run_server(host='0.0.0.0', port=SERVER_PORT):
    with make_server(host, port, application) as httpd:
        print(f'Serving on http://{host}:{port}')
        httpd.serve_forever()


if __name__ == '__main__':
    run_server()
