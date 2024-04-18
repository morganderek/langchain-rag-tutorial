import sys
from PyQt6.QtWidgets import QApplication, QFileDialog, QMessageBox
import pdfplumber
from markdownify import markdownify as md

def pdf_to_markdown(pdf_path, markdown_path):
    """
    Converts the given PDF file to a Markdown file.
    
    Args:
    pdf_path (str): The file path of the source PDF.
    markdown_path (str): The file path where the Markdown file will be saved.
    """
    try:
        with pdfplumber.open(pdf_path) as pdf:
            all_text = ''
            for page in pdf.pages:
                all_text += page.extract_text(x_tolerance=3, y_tolerance=3) + '\n'
            
        markdown_text = md(all_text, heading_style="ATX")
        with open(markdown_path, 'w', encoding='utf-8') as f:
            f.write(markdown_text)
        
        return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def select_pdf():
    """
    Opens a file dialog to select a PDF file.
    """
    dialog = QFileDialog()
    dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
    dialog.setNameFilter("PDF files (*.pdf)")
    if dialog.exec():
        return dialog.selectedFiles()[0]
    return None

def save_markdown():
    """
    Opens a file dialog to specify the filename to save the Markdown file.
    """
    dialog = QFileDialog()
    dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
    dialog.setNameFilter("Markdown files (*.md)")
    dialog.setDefaultSuffix("md")
    if dialog.exec():
        return dialog.selectedFiles()[0]
    return None

def main():
    app = QApplication(sys.argv)
    pdf_path = select_pdf()
    if pdf_path:
        markdown_path = save_markdown()
        if markdown_path:
            success = pdf_to_markdown(pdf_path, markdown_path)
            if success:
                QMessageBox.information(None, "Success", "The file has been converted successfully!")
            else:
                QMessageBox.critical(None, "Failure", "The conversion failed. Check the console for errors.")
        else:
            QMessageBox.warning(None, "Cancelled", "Save operation was cancelled.")
    else:
        QMessageBox.warning(None, "Cancelled", "No PDF file selected.")

if __name__ == "__main__":
    main()
