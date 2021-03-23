import lxml.html as lh


def extract_table_rows_from_html_string(html_string):
    doc = lh.fromstring(html_string)
    tr_elements = doc.xpath('//tr')
    keys = []
    for cell in tr_elements[0]:
        val = cell.text_content()
        keys.append(val.strip())
    rows = []
    for raw_row in tr_elements[1:]:
        row = {}
        for key, cell in zip(keys, raw_row):
            if not key:
                continue
            val = cell.text_content()
            row[key] = val
        rows.append(row)
    return rows
