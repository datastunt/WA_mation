from mysql import connector


def progress_data(data):
    connection = connector.connect(host='datastuntstaging.co.in',
                                   user='u385679644_wpautomation',
                                   password='z>P4I+3L/Q2a',
                                   database='u385679644_wpautomation')
    cursor = connection.cursor()

    try:
        connection.start_transaction()

        # Bulk insert data from logs dictionary into MySQL table
        for entry in data:
            job_id = entry['JobID']
            contact = entry['contact']
            reason = entry['reason']
            timestamp = entry['timestamp']
            # Example SQL query to insert data into a table named 'automation_progress'
            sql = "INSERT INTO automation_progress (JobID, Contact, Reason, Timestamp) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (job_id, contact, reason, timestamp))

        # Commit changes to the database
        connection.commit()

    except connector.Error as err:
        print("Error: ", err)
        connection.rollback()

    finally:
        # Close the database connection
        cursor.close()
        connection.close()


def final_stored_data(data):
    connection = connector.connect(host='datastuntstaging.co.in',
                                   user='u385679644_wpautomation',
                                   password='z>P4I+3L/Q2a',
                                   database='u385679644_wpautomation')
    cursor = connection.cursor()

    try:
        connection.start_transaction()
        # Iterate over each dictionary in the data list
        for entry in data:
            # Extract values from the dictionary
            job_id = entry['JobID']
            contact = entry['contact']
            status = entry['status']
            timestamp = entry['timestamp']

            # Example SQL query to insert data into a table named 'automation_status'
            sql = "INSERT INTO automation_status (JobID, contact_number, Timestamp, Status) VALUES (%s, %s, %s, %s)"
            # Execute the SQL query with values as a tuple
            cursor.execute(sql, (job_id, contact, timestamp, status))
        # Commit changes to the database
        connection.commit()

    except connector.Error as err:
        print("An error occurred during save in database:", err)
        connection.rollback()

    finally:
        # Close the database connection
        cursor.close()
        connection.close()
