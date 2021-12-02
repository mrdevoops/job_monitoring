from flask import Flask,render_template

app = Flask(__name__)

from load_metrics import *

@app.route("/")
def main():
    status_cron_jobs,namespace=load_metrics()
    return render_template('index.html', title='metrics', status_cron_jobs=status_cron_jobs, namespace=namespace)

if __name__ == "__main__":
    app.run(port=8000, host="0.0.0.0", debug="True")
