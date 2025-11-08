# Question File Formats

This guide explains the supported file formats for uploading survey questions.

---

## ✅ Supported File Formats

### 1. **Plain Text (.txt)**

Simple text file with one question per line.

**Example: `questions.txt`**
```
What is your name?
What is your email address?
How satisfied are you with our service?
Would you like to provide additional feedback?
```

**With Question Types:**
```
What is your name? [TEXT]
What is your email address? [TEXT]
How satisfied are you with our service? [MULTIPLE_CHOICE]
- Very Satisfied
- Satisfied
- Neutral
- Dissatisfied
- Very Dissatisfied
Would you like to provide additional feedback? [PARAGRAPH]
```

**Supported Question Types:**
- `[TEXT]` or `[SHORT]` - Short text answer
- `[PARAGRAPH]` or `[LONG]` - Long text answer
- `[MULTIPLE_CHOICE]` or `[RADIO]` - Single choice
- `[CHECKBOX]` - Multiple choice
- `[DROPDOWN]` - Dropdown list

**Options Format:**
Add options on separate lines starting with `-`, `*`, or `•`:
```
Choose your favorite color [MULTIPLE_CHOICE]
- Red
- Blue
- Green
- Yellow
```

---

### 2. **JSON (.json)**

Structured JSON format for more control.

**Example: `questions.json`**
```json
[
  {
    "title": "What is your name?",
    "type": "TEXT",
    "required": true
  },
  {
    "title": "What is your email address?",
    "type": "TEXT",
    "required": true
  },
  {
    "title": "How satisfied are you with our service?",
    "type": "MULTIPLE_CHOICE",
    "required": true,
    "options": ["Very Satisfied", "Satisfied", "Neutral", "Dissatisfied", "Very Dissatisfied"]
  },
  {
    "title": "What features would you like to see?",
    "type": "CHECKBOX",
    "required": false,
    "options": ["Mobile App", "API Access", "Better Reporting", "Integrations"]
  },
  {
    "title": "Please provide any additional feedback",
    "type": "PARAGRAPH",
    "required": false
  }
]
```

**JSON Schema:**
```typescript
{
  "title": string,        // Question text (required)
  "type": string,         // Question type (required)
  "required": boolean,    // Is this question required? (optional, default: false)
  "options": string[]     // Answer options for choice-based questions (optional)
}
```

**Valid Types:**
- `"TEXT"` or `"SHORT_ANSWER"`
- `"PARAGRAPH"` or `"PARAGRAPH_TEXT"` or `"LONG_ANSWER"`
- `"MULTIPLE_CHOICE"` or `"RADIO"`
- `"CHECKBOX"`
- `"DROPDOWN"`

---

### 3. **CSV (.csv)**

Comma-separated values format.

**Example: `questions.csv`**
```csv
Question,Type,Required,Options
What is your name?,TEXT,true,
What is your email address?,TEXT,true,
How satisfied are you with our service?,MULTIPLE_CHOICE,true,"Very Satisfied,Satisfied,Neutral,Dissatisfied,Very Dissatisfied"
What features would you like to see?,CHECKBOX,false,"Mobile App,API Access,Better Reporting,Integrations"
Please provide any additional feedback,PARAGRAPH,false,
```

**Simple CSV (Questions Only):**
If your CSV only has questions in the first column:
```csv
What is your name?
What is your email address?
How satisfied are you with our service?
Would you like to provide additional feedback?
```

---

## ❌ Unsupported File Formats

The following formats are **NOT** supported:

- ❌ **Excel files** (`.xlsx`, `.xls`) - Binary format
- ❌ **Word documents** (`.docx`, `.doc`) - Binary format
- ❌ **PDF files** (`.pdf`) - Binary format
- ❌ **Image files** (`.jpg`, `.png`, etc.)

**Why?** These are binary formats that cannot be directly parsed as text. 

**Workaround:** 
1. Open the file in the respective application
2. Copy the questions
3. Paste into a new `.txt` file
4. Save and upload the `.txt` file

Or use the **Manual Entry** option to paste questions directly.

---

## 📝 Tips for Best Results

### 1. **Use Numbered Lists**
```
1. What is your name?
2. What is your email?
3. How did you hear about us?
```

### 2. **Keep Questions Clear**
- One question per line
- Avoid special characters that might cause parsing issues
- Use UTF-8 encoding for the file

### 3. **Test with a Small File First**
- Start with 2-3 questions
- Verify they parse correctly
- Then upload your full question set

### 4. **Use Manual Entry for Complex Questions**
If you have complex formatting or special requirements, use the **Manual Entry** option where you can:
- See real-time preview
- Edit questions easily
- Add questions one by one

---

## 🔄 Converting Excel to Text

If you have questions in Excel:

1. **Option 1: Copy-Paste**
   - Select the column with questions in Excel
   - Copy (Ctrl+C)
   - Open Notepad
   - Paste (Ctrl+V)
   - Save as `.txt`

2. **Option 2: Save As CSV**
   - In Excel: File → Save As
   - Choose "CSV (Comma delimited) (*.csv)"
   - Upload the CSV file

3. **Option 3: Manual Entry**
   - Just use the "Manual Entry" option in the survey creator
   - Copy questions from Excel
   - Paste directly into the questions field

---

## 📚 Example Files

### Minimal Text File
```
What is your name?
What is your email?
How can we improve?
```

### Complete Text File with Types
```
1. Contact Information

What is your full name? [TEXT]
What is your email address? [TEXT]
What is your phone number? [TEXT]

2. Satisfaction Survey

How satisfied are you with our service? [MULTIPLE_CHOICE]
- Very Satisfied
- Satisfied
- Neutral
- Dissatisfied
- Very Dissatisfied

What aspects did you like most? [CHECKBOX]
- Product Quality
- Customer Service
- Pricing
- Delivery Speed
- User Interface

Which department helped you? [DROPDOWN]
- Sales
- Support
- Technical
- Billing

3. Feedback

Please provide detailed feedback [PARAGRAPH]

Would you recommend us to others? [MULTIPLE_CHOICE]
- Yes, definitely
- Yes, probably
- Not sure
- Probably not
- Definitely not
```

---

## 🆘 Troubleshooting

### "Failed to parse file"
- Check file encoding (should be UTF-8)
- Ensure file is not empty
- Verify it's a text-based format (.txt, .json, .csv)

### "No questions found in file"
- Make sure there's text content
- Check that questions aren't just whitespace
- Verify line endings (use Unix or Windows format)

### "Invalid JSON"
- Validate your JSON at [jsonlint.com](https://jsonlint.com)
- Check for missing commas or brackets
- Ensure proper quote usage

### "Binary file not supported"
- You uploaded an Excel/Word/PDF file
- Convert to text format first (see above)

---

## 💡 Best Practice

For the best experience:

1. **Start Simple**: Use plain text with one question per line
2. **Add Types Later**: Once basic parsing works, add `[TYPE]` markers
3. **Use JSON for Complex**: If you need full control, use JSON format
4. **Test Small**: Always test with a few questions first

---

**Need Help?** Use the **Manual Entry** option - it's often easier than preparing a file!
