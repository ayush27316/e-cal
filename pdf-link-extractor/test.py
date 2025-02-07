import fitz  # PyMuPDF

def highlight_lines(pdf_path, lines_to_highlight):
    # Open the local PDF file using PyMuPDF
    pdf_document = fitz.open(pdf_path)

    # Iterate through pages
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]

        # Iterate through lines to highlight
        for line_number in lines_to_highlight.get(page_num, []):
            # Get the rect coordinates of the line
            rect = page.select_line(line_number)

            # Highlight the line with a rectangle
            highlight = page.add_highlight_annot(rect)

            # Set the color of the highlight (you can customize this)
            highlight.set_colors({"stroke": (1, 0, 0), "fill": (1, 0, 0)})

    # Save the modified PDF with highlights
    modified_pdf_path = "out/highlighted_pdf.pdf"
    pdf_document.save(modified_pdf_path)
    pdf_document.close()



# Example usage
pdf_path = "ug.pdf"
lines_to_highlight = {
    58: [10, 20],  # Highlight lines on page 1 (0-based index)
    59: [5, 15],   # Highlight lines on page 2
    # Add more pages and line numbers as needed
}

highlight_lines(pdf_path, lines_to_highlight)
