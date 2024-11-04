from flask import Flask, render_template, request, send_file, redirect, url_for, session
from fpdf import FPDF
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for session management

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(200, 10, 'Professional Resume', ln=True, align='C')
        self.ln(10)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.set_text_color(0, 51, 153)  # Dark blue color
        self.cell(0, 10, title, 0, 1, 'L')
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, body)
        self.ln()

    def add_section(self, title, content):
        self.chapter_title(title)
        self.chapter_body(content)

    def add_border(self):
        self.set_fill_color(255, 255, 255)
        self.rect(5, 5, 200, 287, style='D')  # Page border

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_resume():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    address = request.form['address']
    degree = request.form['degree']
    university = request.form['university']
    year = request.form['year']
    job_title = request.form['job_title']
    company = request.form['company']
    duration = request.form['duration']
    responsibilities = request.form['responsibilities']
    skills = request.form['skills']

    pdf = PDF()
    pdf.add_page()

    pdf.add_border()  # Add border to PDF
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, name, ln=True)
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, f"Email: {email}", ln=True)
    pdf.cell(0, 10, f"Phone: {phone}", ln=True)
    pdf.cell(0, 10, f"Address: {address}", ln=True)

    pdf.add_section('Profile Summary', 'Motivated engineering student with a strong background in AI and real-world project experience...')
    pdf.add_section('Experience', f'{job_title} at {company} ({duration})')
    pdf.add_section('Education', f'{degree}, {university}, Year: {year}')
    pdf.add_section('Skills', skills)

    # Store the filename in a predictable location
    pdf_file = os.path.join(os.getcwd(), f"{name}_resume.pdf")
    pdf.output(pdf_file)

    # Debugging: Check if the PDF file was created
    print(f"PDF generated at: {pdf_file}")
    print(f"File exists: {os.path.exists(pdf_file)}")

    # Store the filename in the session for later removal
    session['pdf_file'] = pdf_file

    return redirect(url_for('download_page', file_name=f"{name}_resume.pdf"))

@app.route('/download/<file_name>')
def download_page(file_name):
    return render_template('download.html', file_name=file_name)

@app.route('/download_file/<file_name>')
def download_file(file_name):
    # Construct the file path
    pdf_file_path = os.path.join(os.getcwd(), file_name)  # Ensure correct path
    print(f"Attempting to download file at: {pdf_file_path}")  # Debugging statement

    if os.path.exists(pdf_file_path):
        return send_file(pdf_file_path, as_attachment=True)
    else:
        print("File not found!")  # Debugging statement
        return "File not found", 404  # Return a 404 error if the file doesn't exist

@app.after_request
def remove_pdf(response):
    try:
        pdf_file = session.get('pdf_file')  # Retrieve the filename from the session
        if pdf_file and os.path.exists(pdf_file):  # Check if the file exists before removing
            os.remove(pdf_file)
            print(f"Removed file: {pdf_file}")  # Debugging statement
    except Exception as e:
        print(f"Error deleting file: {e}")
    return response

if __name__ == '__main__':
    app.run(debug=True)
