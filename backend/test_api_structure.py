"""
Test script to analyze the Google Forms API request structure
"""
import json
from google_forms_service import GoogleFormsService

# Initialize service
service = GoogleFormsService()

# Sample questions
questions = [
    {
        "title": "What is your name?",
        "type": "TEXT",
        "required": True
    },
    {
        "title": "Choose your favorite color",
        "type": "MULTIPLE_CHOICE",
        "required": True,
        "options": ["Red", "Blue", "Green"]
    }
]

print("=" * 80)
print("ANALYZING GOOGLE FORMS API REQUEST STRUCTURE")
print("=" * 80)

# Manually build the requests to see the structure
requests = []

for idx, question in enumerate(questions):
    question_type = question.get("type", "TEXT").upper()
    title = question.get("title", f"Question {idx + 1}")
    required = question.get("required", False)
    options = question.get("options", [])
    
    print(f"\nQuestion {idx + 1}: {title}")
    print(f"  Type: {question_type}")
    print(f"  Required: {required}")
    if options:
        print(f"  Options: {options}")
    
    # Build the question body with required field and type
    question_body = {
        "required": required
    }
    
    # Handle different question types
    if question_type in ["TEXT", "SHORT_ANSWER"]:
        question_body["textQuestion"] = {
            "paragraph": False
        }
    elif question_type in ["PARAGRAPH", "PARAGRAPH_TEXT", "LONG_ANSWER"]:
        question_body["textQuestion"] = {
            "paragraph": True
        }
    elif question_type == "MULTIPLE_CHOICE":
        question_body["choiceQuestion"] = {
            "type": "RADIO",
            "options": [{"value": opt} for opt in options]
        }
    elif question_type == "CHECKBOX":
        question_body["choiceQuestion"] = {
            "type": "CHECKBOX",
            "options": [{"value": opt} for opt in options]
        }
    elif question_type == "DROPDOWN":
        question_body["choiceQuestion"] = {
            "type": "DROP_DOWN",
            "options": [{"value": opt} for opt in options]
        }
    
    # Create the request structure
    request_item = {
        "createItem": {
            "item": {
                "title": title,
                "questionItem": {
                    "question": question_body
                }
            },
            "location": {
                "index": idx
            }
        }
    }
    
    requests.append(request_item)
    
    print("\n  API Request Structure:")
    print(json.dumps(request_item, indent=4))

print("\n" + "=" * 80)
print("COMPLETE BATCH UPDATE BODY")
print("=" * 80)

update_body = {
    "requests": requests
}

print(json.dumps(update_body, indent=2))

print("\n" + "=" * 80)
print("VALIDATION CHECKS")
print("=" * 80)

# Validate structure
for idx, req in enumerate(requests):
    print(f"\nRequest {idx + 1} Validation:")
    
    # Check if title is at correct level
    if "title" in req["createItem"]["item"]:
        print("  ✅ 'title' is at item level")
    else:
        print("  ❌ 'title' is missing at item level")
    
    # Check if questionItem exists
    if "questionItem" in req["createItem"]["item"]:
        print("  ✅ 'questionItem' exists")
        
        # Check if question exists
        if "question" in req["createItem"]["item"]["questionItem"]:
            print("  ✅ 'question' exists inside questionItem")
            
            question_obj = req["createItem"]["item"]["questionItem"]["question"]
            
            # Check if required is in question
            if "required" in question_obj:
                print("  ✅ 'required' is inside question object")
            else:
                print("  ❌ 'required' is missing from question object")
            
            # Check if question type exists
            if "textQuestion" in question_obj or "choiceQuestion" in question_obj:
                print("  ✅ Question type (textQuestion/choiceQuestion) is inside question object")
            else:
                print("  ❌ Question type is missing from question object")
        else:
            print("  ❌ 'question' is missing from questionItem")
    else:
        print("  ❌ 'questionItem' is missing from item")

print("\n" + "=" * 80)
print("STRUCTURE SUMMARY")
print("=" * 80)
print("""
Correct Google Forms API Structure:
{
  "createItem": {
    "item": {
      "title": "Question text here",           ← title at item level
      "questionItem": {
        "question": {                          ← question object
          "required": true,                    ← required inside question
          "textQuestion": {                    ← question type inside question
            "paragraph": false
          }
        }
      }
    },
    "location": {
      "index": 0
    }
  }
}
""")

print("=" * 80)
print("POTENTIAL ERROR CAUSES")
print("=" * 80)

error_checks = [
    ("Incorrect nesting of 'required' field", "Should be inside 'question' object, not at item level"),
    ("Incorrect nesting of question type", "Should be inside 'question' object, not at item level"),
    ("Missing 'title' at item level", "Title should be directly under 'item', not under 'question'"),
    ("Incorrect permission role for 'anyone'", "Should use 'reader' role, not 'writer'"),
    ("Service account not sharing with owner", "Form won't appear in creator's Drive"),
    ("Google Forms API not enabled", "Check Google Cloud Console"),
    ("Service account lacks permissions", "Check IAM roles in Cloud Console"),
    ("API quota exceeded", "Check quotas in Cloud Console"),
]

for idx, (error, solution) in enumerate(error_checks, 1):
    print(f"{idx}. {error}")
    print(f"   Solution: {solution}")

print("\n" + "=" * 80)
