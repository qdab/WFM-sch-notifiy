# WFM-sch-notifiy

This project aims to send Microsoft Exchange emails based on schedule data from an Excel or CSV file. The repository now includes a minimal web server implemented with Python's standard library.

## Quick Start

1. Create or update `schedule.csv` with your schedule entries (Date, Task).
2. Optionally set `SCHEDULE_FILE` to point to a different path.
3. (Optional) set `SCHEDULE_URL` to a CSV download link from Excel Online to
   automatically fetch the latest schedule.
4. Run the server:
   ```bash
   python server.py
   ```
5. Open `http://localhost:8000` in your browser to view the upcoming schedule.

### Configuration

Environment variables tweak the server:

* `SCHEDULE_FILE` - path to the CSV file
* `SCHEDULE_URL` - URL to download the CSV on each request
* `PORT` - port the web server listens on (default `8000`)
* `DAYS_AHEAD` - number of days of tasks to display (default `7`)

### Email Notifications

Use `notify.py` to send a daily email for tasks scheduled for today:

```bash
python notify.py
```

Configure SMTP settings via these environment variables:

* `SMTP_HOST` and `SMTP_PORT`
* `SMTP_USER` and `SMTP_PASS` if authentication is required
* `FROM_ADDR` and `TO_ADDR`

This script can be invoked via `cron` to run each morning:

```
0 6 * * * /usr/bin/python /path/to/notify.py
```

The web server reads `SCHEDULE_FILE` or downloads from `SCHEDULE_URL` on each
request and shows the upcoming schedule in a table.
