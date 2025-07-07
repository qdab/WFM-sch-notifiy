import csv
import os
from urllib.request import urlopen
from wsgiref.simple_server import make_server

SCHEDULE_FILE = 'schedule.csv'
SCHEDULE_URL = os.environ.get('SCHEDULE_URL')

def load_schedule(path=SCHEDULE_FILE):
    entries = []
    try:
        if SCHEDULE_URL:
            stream = urlopen(SCHEDULE_URL)
        else:
            stream = open(path, 'rb')
        with stream as raw:
            reader = csv.reader(line.decode('utf-8') for line in raw)
            header = next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    entries.append({'date': row[0], 'task': row[1]})
    except FileNotFoundError:
        pass
    except Exception:
        pass
    return entries


def render_table(entries):
    rows = '\n'.join(f'<tr><td>{e["date"]}</td><td>{e["task"]}</td></tr>' for e in entries)
    return f"""<html><body>
<h1>Schedule</h1>
<table border='1'>
<tr><th>Date</th><th>Task</th></tr>
{rows}
</table>
</body></html>"""


def application(environ, start_response):
    entries = load_schedule()
    content = render_table(entries)
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    return [content.encode('utf-8')]


def run_server(host='0.0.0.0', port=8000):
    with make_server(host, port, application) as httpd:
        print(f'Serving on http://{host}:{port}')
        httpd.serve_forever()


if __name__ == '__main__':
    run_server()
