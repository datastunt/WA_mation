import threading
from engine import *
from flask import Flask, render_template, request, Response

app = Flask(__name__)
data = {}


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/automation", methods=['POST'])
def automation():
    global data
    media = request.files.get('media_content')
    text = request.form.get('message')
    bulk_file = request.files.get('bulkFile')
    result = run_automation(bulk_file, media, text)
    if result is not None:
        data = dict(result)
        return render_template('logs_table.html', result=data)
    else:
        return render_template('logs_table.html', result=data)

    # automation_thread = threading.Thread(target=run_automation(bulk_file, media, text), args=(bulk_file, media, text))
    # automation_thread.start()


@app.route("/kill_automation", methods=['GET'])
def kill_automation_route():
    kill_automation()
    return render_template('index.html')


@app.route('/download_pdf')
def download_pdf():
    # Combine completed and uncompleted job data
    main_data = {'Done task': data['completed_job'], 'Undone task': data['uncompleted_job']}
    # Efficient DataFrame creation
    rows = []
    for key, values in main_data.items():
        for item in values:
            rows.append({
                'JobID': item['JobID'],
                'Sent to': item.get('contact', ''),
                'Status': item.get('status', 'Undone'), # Use 'Undone' for tasks without a 'status'
                'Reason': item.get('reason', ''),
                'Timestamp': item['timestamp']
            })
    df = pd.DataFrame(rows)
    # Generate PDF
    pdf = generate_pdf(df)
    # Set up response
    response = Response(
        pdf,
        mimetype='application/pdf',
        headers={'Content-Disposition': 'attachment; filename=data.pdf'}
    )
    return response

# @app.route('/download_pdf')
# def download_pdf():
#     # Generate DataFrame from sample data
#     df = pd.DataFrame(list(data.items()), columns=['JobID', 'Sent to', 'status', 'timestamp'])
#     # Set up response to send PDF as a file download
#     response = Response(
#         generate_pdf(df),
#         mimetype='text/pdf',
#         headers={'Content-Disposition': 'attachment; filename=data.pdf'}
#     )
#     return response

# for recipients
# recipients = request.form.get('recipients')
# recipients = recipients.split("\n") if recipients else []
# recipients = [name.strip() for name in recipients if name.strip()]


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)



#
# import threading
# from engine import *
# from flask import Flask, render_template, request, Response
# app = Flask(__name__)
# data = {}
# @app.route("/")
# def home():
#     return render_template('index.html')
# def start_automation_thread(bulk_file, media, text):
#     global data
#     result = run_automation(bulk_file, media, text)
#     if result is not None:
#         data = dict(result)
# @app.route("/automation", methods=['POST'])
# def automation():
#     global data
#     media = request.files.get('media_content')
#     text = request.form.get('message')
#     bulk_file = request.files.get('bulkFile')
#     # Start the automation task in a separate thread
#     automation_thread = threading.Thread(target=start_automation_thread, args=(bulk_file, media, text))
#     automation_thread.start()
#     return render_template('logs_table.html', result=data)









