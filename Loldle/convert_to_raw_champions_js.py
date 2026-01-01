JS_FILE = "app.js"
OUT_FILE = "champions_raw.js"

with open(JS_FILE, encoding="utf-8") as f:
    js = f.read()

def extract_js_array(js_text, var_name="Nc"):
    start = js_text.find(f"{var_name}=")
    if start == -1:
        raise ValueError(f"Không tìm thấy {var_name}=")

    # Tìm dấu '[' đầu tiên
    start = js_text.find("[", start)
    if start == -1:
        raise ValueError("Không tìm thấy '['")

    bracket_count = 0
    end = start

    while end < len(js_text):
        if js_text[end] == "[":
            bracket_count += 1
        elif js_text[end] == "]":
            bracket_count -= 1
            if bracket_count == 0:
                return js_text[start:end + 1]
        end += 1

    raise ValueError("Không tìm thấy ']' kết thúc")


champions_js = extract_js_array(js, "Nc")

with open(OUT_FILE, "w", encoding="utf-8") as f:
    f.write(champions_js)

print("✅ Extracted FULL champion array")
print("Length:", len(champions_js))
