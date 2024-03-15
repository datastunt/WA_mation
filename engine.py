import io
import os
import random
import string
import sys

import matplotlib
import pandas as pd
# from main import data
from datetime import datetime
from matplotlib import pyplot as plt
from playwright.sync_api import sync_playwright
from data_layer import final_stored_data, progress_data

matplotlib.use('Agg')
terminate_flag = False
completed_task = []
uncompleted_task = []
user_data_path_ = "\\Default_WA_personal_whatsapp"
logs = {}


def run_automation(bulk_file, media, text):
    try:
        if not terminate_flag:
            with sync_playwright() as p:
                context = p.firefox.launch_persistent_context(user_data_path_, headless=False)
                page = context.new_page()
                page.goto('https://web.whatsapp.com')
                page.wait_for_load_state("load")
                page.wait_for_timeout(5000)

                if media:
                    media.save(media.filename)
                    media = media.filename
                else:
                    media = None

                if bulk_file and not terminate_flag:
                    try:
                        bulk_file.save(bulk_file.filename)
                        bulk_file = bulk_file.filename  # save the bulk file in local
                        all_sheets_data = pd.read_excel(bulk_file, sheet_name=None)  # convert into dictionary
                        contacts_list = []
                        for sheet_name, sheet_data in all_sheets_data.items():
                            if sheet_data is not None and not sheet_data.empty:
                                for index, row in sheet_data.iterrows():
                                    contacts_list.append(
                                        (row['Name'], row['Number']))  # Store name and number as a tuple
                            else:
                                print(f"Sheet {sheet_name} is empty or not readable.")

                        for name, number in contacts_list:
                            number = str(number)
                            if not terminate_flag:
                                selector = 'div._3ndVb.fbgy3m38.ft2m32mm.oq31bsqd.nu34rnf1[title="New chat"]'
                                page.wait_for_selector(selector)
                                page.click(selector)
                                page.wait_for_timeout(2000)
                                selector2 = "p.selectable-text.copyable-text.iq0m558w.g0rxnol2"
                                page.fill(selector2, number)
                                page.wait_for_timeout(5000)
                                try:
                                    selector_unavbl = 'span._11JPr'
                                    contact_unavbl = page.inner_text(selector_unavbl)
                                    condition = f"No results found for '{number}'"
                                    if selector_unavbl == condition or contact_unavbl == condition:
                                        page.wait_for_selector('div.kk3akd72.dmous0d2.fewfhwl7.ajgl1lbb.ltyqj8pj')
                                        page.click('div.kk3akd72.dmous0d2.fewfhwl7.ajgl1lbb.ltyqj8pj')
                                        page.wait_for_timeout(2000)
                                        timestamp = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
                                        jobid = generate_job_id()
                                        uncompleted_task.append({'JobID': jobid,
                                                                 'contact': number,
                                                                 'reason': "Unavailable on WhatsApp.",
                                                                 'timestamp': timestamp
                                                                 })
                                    else:
                                        page.keyboard.press('Enter')
                                        page.wait_for_timeout(2000)
                                        if media is not None and not terminate_flag:
                                            selector3 = 'div._3ndVb[aria-label="Attach"]'
                                            page.click(selector3)
                                            page.wait_for_timeout(2000)
                                            file_input = page.locator(
                                                'input[accept="image/*,video/mp4,video/3gpp,video/quicktime"]')
                                            file_input.set_input_files(media)
                                            page.wait_for_timeout(3000)
                                        if text is not None and not terminate_flag:
                                            selector5 = 'div[title="Type a message"]'
                                            page.wait_for_selector(selector5)
                                            text_data = f" नमस्ते {name},\n" + text
                                            page.fill(selector5, text_data)
                                        page.wait_for_timeout(4000)
                                        page.keyboard.press('Enter')
                                        timestamp = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
                                        page.wait_for_timeout(5000)
                                        jobid = generate_job_id()
                                        completed_task.append({'JobID': jobid,
                                                               'contact': number,
                                                               'status': 'Done',
                                                               'timestamp': timestamp
                                                               })
                                except Exception as err:
                                    print("error during sending message:", err)
                            else:
                                sys.exit()
                        logs['completed_job'] = completed_task
                        logs['uncompleted_job'] = uncompleted_task
                        final_stored_data(completed_task)
                        progress_data(uncompleted_task)
                        page.wait_for_timeout(10000)
                        print('Successfully Bulk file is executed....JOB COMPLETE\n', "Done task : ",
                              completed_task, '\n', "Undone task : ", uncompleted_task)
                        context.close()
                        return logs
                    except Exception as err:
                        return print("Error in bulk method", err)
                    # except TimeoutError:

                    # except Exception as err:
                    #     return print("Error in bulk method", err)
                    finally:
                        os.remove(bulk_file)
                        # if media:
                        #     os.remove(media)
                else:
                    context.close()
        else:
            exit()
    except Exception as err:
        print("Error occurred during execution of job:", err)
    finally:
        if media:
            os.remove(media)


def kill_automation():
    global terminate_flag
    terminate_flag = True
    return terminate_flag


def generate_job_id():
    alphabet = string.ascii_uppercase
    current_date = datetime.now().strftime('%d-%m-%Y')  # Get current date
    random_string = ''.join(random.choices(alphabet, k=6))  # Generate a random string of alphabets
    job_id = f"JOB-{current_date}-{random_string}"  # Combine current date and random string
    return job_id


def generate_pdf(df):
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('tight')
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(8)  # Adjust font size as needed
    table.scale(1, 1.5)  # Adjust table scale for better fit in PDF
    # Save the figure as a PDF to a bytes buffer
    pdf_output = io.BytesIO()
    plt.savefig(pdf_output, format='pdf', bbox_inches='tight')
    pdf_output.seek(0)
    plt.close(fig)
    return pdf_output.getvalue()


