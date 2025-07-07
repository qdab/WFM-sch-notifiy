# WFM-sch-notifiy

This project aims to send Microsoft Exchange emails based on schedule data from an Excel or CSV file. The repository now includes a minimal web server implemented with Python's standard library.

## Quick Start

1. Create or update `schedule.csv` with your schedule entries (Date, Task).
2. (Optional) set `SCHEDULE_URL` to a CSV download link from Excel Online to
   automatically fetch the latest schedule.
3. Run the server:
   ```bash
   python server.py
   ```
4. Open `http://localhost:8000` in your browser to view the schedule table.

### Email Notifications

Use `notify.py` to send a daily email for tasks scheduled for today:

```bash
python notify.py
```

Configure SMTP settings via the `SMTP_HOST`, `SMTP_PORT`, `FROM_ADDR` and
`TO_ADDR` environment variables.

The server reads `schedule.csv` (or downloads from `SCHEDULE_URL`) on each
request and displays it as an HTML table.
