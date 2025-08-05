from app.celery_app import app
import pdfkit
import os
import datetime

@app.task()  # bind=True allows access to self.request.id
def generate_pdf(data: dict):
    html_out = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
            <meta charset="UTF-8" />
            <title>User Info Display</title>
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            </head>
            <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f4f4f4;">

            <h1 style="text-align: center; color: #333;">User Information</h1>

            <div style="background-color: #fff; padding: 20px; border-radius: 5px; border: 1px solid #ccc; max-width: 500px; margin: 0 auto;">
                  <div style="margin-bottom: 15px;">
                  <strong style="display: inline-block; width: 100px;">Name:</strong>
                  <span>{data['name']}</span>
                  </div>

                  <div style="margin-bottom: 15px;">
                  <strong style="display: inline-block; width: 100px;">Email:</strong>
                  <span>{data['email']}</span>
                  </div>

                  <div style="margin-bottom: 15px;">
                  <strong style="display: inline-block; width: 100px;">Password:</strong>
                  <span>{data['password']}</span>
                  </div>

                  <div style="margin-bottom: 15px;">
                  <strong style="display: inline-block; width: 100px;">Description:</strong>
                  <div style="margin-left: 100px;">
                  <p style="margin: 0;">{data['desc']}</p>
                  </div>
                  </div>
            </div>

            </body>
            </html>
            """

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    unqiue_id = datetime.datetime.now()
    output_path = os.path.join(output_dir, f"{data['name']}_{unqiue_id}_report.pdf")

    pdfkit.from_string(html_out, output_path)
    return output_path
