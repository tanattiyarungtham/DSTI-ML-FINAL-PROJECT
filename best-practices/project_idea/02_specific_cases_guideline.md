 NLP Modules – Technical Implementation with Mixtral-8x7B-Instruct

For fine-tuning Mixtral using Axolotl with Alpaca or ChatML format, JSON structure :

```json
{
  "instruction": "<USER MESSAGE>",
  "input": "",
  "output": <EXPECTED FULL OUTPUT>
}
```

### I. Task Type Detection (Structured Log vs. Recommendation)

**Goal**

Automatically determine whether the user input should:
- Generate a structured activity/meal log (JSON output)
- Trigger a personalized recommendation (free-form text)	
- Start a follow-up question to clarify missing info

**How to implement**
- Fine-tune Mixtral using labeled examples that include a field like:

#### Log activity :

```json
{
  "instruction": "I ran for 30 minutes this morning and ate two bananas after.",
  "input": "",
  "output": {
    "task_type": "log_activity",
    "activity": {
      "type": "running",
      "duration": "30 minutes",
      "intensity": "moderate",
      "moment": "morning"
    },
    "meals": [
      {
        "label": "snack",
        "time": "after training",
        "foods": [
          { "food": "banana", "quantity": "2" }
        ]
      }
    ]
  }
}
```
#### Advice

```json
{
  "instruction": "I train CrossFit 5x/week and want to lose fat. Any advice?",
  "input": "",
  "output": {
    "task_type": "give_advice",
    "advice": "To optimize fat loss with CrossFit, reduce evening carbs and increase protein intake to 2g/kg body weight..."
  }
}
```

#### Ask Clarification

```json
{
  "instruction": "I had chicken.",
  "input": "",
  "output": {
    "task_type": "ask_clarification",
    "follow_up": "How much chicken did you eat? 150g like usual?"
  }
}
```

#### Several in one time 



Fully feasable with Mixtral (fine-tuned using Axolotl)

---

### 2. Entity Extraction & Schema Switching (LLM-based NER)

**Goal**

Extract structured data like:
- Activity type (e.g., “muscle_training”)	
- Foods, quantities, time, brand 
- And adapt schema dynamically (e.g., switch to gym schema if activity = “muscle_training”)

**How to implement**
- Fine-tune Mixtral using text → JSON mappings, including nested examples:

```json
{
  "instruction": "This evening I did a 1-hour muscle training session with bench press: 10 reps at 70kg, 90s rest.",
  "input": "",
  "output": {
    "activity": {
      "type": "muscle_training",
      "duration": "1h",
      "intensity": "intense",
      "moment": "evening",
      "exercises": [
        {
          "name": "bench press",
          "sets": [
            { "reps": 10, "weight": "70kg", "rest": "90s" }
          ]
        }
      ]
    },
    "meals": []
  }
}
```

Backend uses rules like:

```python
if activity["type"] == "muscle_training":
    use_template("gym")
```
All logic is handled by fine-tuned Mixtral + Python backend

---

### 3. Granular Normalization (Only for Dates & Times)

**Goal**
- Normalize vague expressions like "this morning", "before the gym" into explicit values 
- Distinguish time labels: "breakfast", "post-workout snack" with actual timestamps

**How to implement**
- Fine-tune Mixtral to: 
  - Predict "label": "breakfast" or "time": "08:00" 
  - Or auto-clarify:
    
  	“Do you mean breakfast or morning snack?” 

- Use time-aware prompt templates:
```
Current time: 14:30. Last meal recorded: 12:00.
```

```json
{
  "instruction": "I had a snack this morning.",
  "input": "Current time is 15:45. Last meal was lunch at 12:00.",
  "output": {
    "activity": null,
    "meals": [
      {
        "label": "snack",
        "time": "10:00",
        "foods": [ ... ]
      }
    ]
  }
}
```

- Optionally use dateparser or arrow Python libs to interpret edge cases.

--- 

### 4. User History & Habit Detection

**Goal**

Identify patterns such as:
- Repeating meals (e.g., oatmeal every Monday breakfast) 
- Consistent training slots (e.g., gym Monday 6pm) 
- Use them to autofill or improve recommendations

**How to implement**
- Store structured logs per user:

```json
"user_profile": {
  "Monday_breakfast": ["oatmeal", "banana"],
  "Monday_evening_training": "muscle_training"
}
```

- Inject this into prompts:

```json
"context": "User typically eats oatmeal on Monday at 08:00."
```

- Let Mixtral incorporate it in advice or JSON completion

- Requires basic user DB (SQLite, MongoDB, JSON) + prompt building

---

### 5. Missing Information Handling & Auto-Follow-up

**Goal**

Detect when critical fields are missing (e.g., no quantity) and ask for clarification

**How to implement**
- Fine-tune Mixtral using chat format:

```json
[
  {"role": "user", "content": "I had chicken"},
  {"role": "assistant", "content": "How much chicken? 150g as usual?"}
]
```

```json
{
    "time": "after training",
    "foods": [
        { "food": "chicken" }
    ]
}
```

- Or detect missing fields in Python and re-prompt:

```python
for food_entry in meal["foods"]:
    if "quantity" not in food_entry:
        food_name = food_entry.get("food", "this food")
        ask_user(f"How much {food_name} did you eat?")
```

- Fully feasible with Mixtral + optional rule-based fallback

---

### 6. Validation (Sanity Checks)

**Goal**

Prevent impossible values, e.g.:
- Negative quantities
- Unrealistic weights (e.g., 1e999 kg of pasta)
- Empty or malformed fields

**How to implement**

- Use Pydantic or manual validation:

```python
import re 

qty = "150kg"

match = re.match(r"(\d+(\.\d+)?)", qty)
if match and float(match.group(1)) > 1000:
    raise ValueError("Too much quantity")
```

- Return correction prompt:

```
“Did you mean 150g of chicken instead of 150kg?”
```

- Fully handled via Python after LLM output

--- 

### 7. User Embedding + Similarity-Based Recommendation

Goal
- Identify similar user profiles (goals + habits)
- Retrieve and inject their past recommendations

How to implement
- Convert user profile into vector using sentence-transformers

```json
{
  "goal": "muscle gain",
  "training": "3x/week strength + 2x cardio",
  "usual_meals": ["chicken", "rice", "veggies"]
}
```

- Store embeddings in FAISS index 
- On new prompt: search nearest neighbor, inject their best plan as context into Mixtral

Requires FAISS + sentence-transformers (all can run offline)

