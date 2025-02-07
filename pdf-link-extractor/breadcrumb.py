import re
import xlsxwriter
import pandas as pd
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

def filter_links(text):
    """
    Extracts root and terminal links from the given text.
    Filters out links containing 'Minerva'.
    """
    regex = r"Minerva"
    index_list = [i for i, char in enumerate(text) if char == ">"]
    
    if not index_list:
        return None
    
    root_str = text[:index_list[0]].lstrip(":")
    terminal_str = text[index_list[-1] + 1:].lstrip(":")
    
    if re.search(regex, root_str):
        return None
    
    return [root_str, terminal_str]

def is_breadcrumbs(line_text):
    """
    Checks if a given line of text contains breadcrumbs (identified by '>').
    """
    return ">" in line_text

def extract_breadcrumbs_from_pdf(pdf_path, output_excel):
    """
    Extracts breadcrumbs and corresponding sections from a PDF file and saves them in an Excel file.
    """
    result = []  # List to store extracted breadcrumb data
    page_number = 1  # Tracks current page number
    ix = 1  # Page index counter
    iy = 0  # Iteration counter for elements
    target_str = ""  # Holds extracted breadcrumb text
    section = ""  # Holds section header
    
    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                page_text = [t_line.get_text() for t_line in element]
                
                for i, line in enumerate(page_text):
                    if not line.strip() or line.startswith(">"):
                        continue
                    
                    # Check if the last line contains breadcrumbs
                    if i == len(page_text) - 1:
                        if is_breadcrumbs(line):
                            target_str += "".join(
                                character.get_text()
                                for it_line in element
                                for character in it_line
                                if isinstance(character, LTChar) and (character.fontname == "Times-Italic" or character.get_text() == ">")
                            )
                    else:
                        # Check for breadcrumbs within the text block
                        if is_breadcrumbs(line):
                            target_str += "".join(
                                character.get_text()
                                for it_line in element
                                for character in it_line
                                if isinstance(character, LTChar) and (character.fontname == "Times-Italic" or character.get_text() in {">", ":"})
                            )
                            
                            # Check next line to confirm breadcrumbs continuation
                            if any(
                                isinstance(character, LTChar) and character.fontname != "Times-Italic" and character.get_text() not in {">", ":"}
                                for character in element[i + 1]
                            ):
                                break
                            
                            # Append next line content if necessary
                            target_str += "".join(
                                character.get_text()
                                for character in element[i + 1]
                                if isinstance(character, LTChar) and (character.fontname == "Times-Italic" or character.get_text() in {">", ":"})
                            )
                    
                    # If breadcrumbs were extracted, determine the corresponding section
                    if target_str:
                        for prev_element in page_layout:
                            if isinstance(prev_element, LTTextContainer) and iy > (ix - 2):
                                break
                            for ptext_line in prev_element:
                                if any(
                                    isinstance(character, LTChar) and character.fontname == "Helvetica-Bold" and character.size >= 8.0
                                    for character in ptext_line
                                ):
                                    section = ptext_line.get_text()
                                    break
                            iy += 1
                        
                        # If no section was found, check the previous page
                        if not section:
                            for p_page_layout in extract_pages(pdf_path, page_numbers=[page_number - 2]):
                                for pelement in p_page_layout:
                                    if isinstance(pelement, LTTextContainer):
                                        for pptext_line in pelement:
                                            if any(
                                                isinstance(character, LTChar) and character.fontname == "Helvetica-Bold" and character.size >= 8.0
                                                for character in pptext_line
                                            ):
                                                section = pptext_line.get_text()
                                                break
                        
                        # Filter extracted breadcrumbs and store results
                        ret_str = filter_links(target_str)
                        if ret_str:
                            result.append({
                                'page_number': page_number,
                                'section': section,
                                'root_link': ret_str[0],
                                'terminal_link': ret_str[1]
                            })
                        
                        # Reset temporary variables for next extraction
                        target_str = ""
                        section = ""
                        iy = 0
        
        ix += 1
        page_number += 1
    
    # Convert extracted data into a DataFrame and save as an Excel file
    df = pd.DataFrame(result, columns=['page_number', 'section', 'root_link', 'terminal_link'])
    df.to_excel(output_excel, engine='xlsxwriter')

# Example usage
extract_breadcrumbs_from_pdf("ug.pdf", "table_bread.xlsx")
