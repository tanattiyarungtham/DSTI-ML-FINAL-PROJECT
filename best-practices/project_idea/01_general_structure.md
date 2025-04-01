
The fine-tuned Mixtral-8x7B-Instruct model dynamically recognizes activity and meal patterns in natural language and structures them into a detailed JSON format. 

Based on the identified sport (e.g., muscle training, sprint), it adapts the schema and adds the appropriate nested fields — 
such as exercises with sets and weights for gym sessions, or sprint repetitions with rest times. 

Additional extensions can later support other sports like swimming or tennis, and even competition results.

Meal entries include food names, quantities, and optional references (e.g., brands), enabling detailed tracking and personalized analysis.

```json
{
  "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
  "fine_tuning": {
    "framework": "Axolotl",
    "technique": "QLoRA",
    "format": "Alpaca / ChatML", (https://zackproser.com/blog/how-to-create-a-custom-alpaca-dataset)
    "hardware_min": "1x A100 80GB or 2x RTX 3090",
    "dataset_path": "data/dataset.jsonl"
  }, 
```

```json
  "schema": {
    "activity": {
      "type": "string",
      "duration": "string (e.g. '30 minutes')",
      "intensity": "string (e.g. 'moderate')",
      "moment": "string (e.g. morning, evening)",
      "details_by_sport": {
        "muscle_training": {
          "exercises": [
            {
              "name": "string",
              "sets": [
                {"reps": "int", "weight": "string", "rest": "string"}
              ]
            }
          ]
        },
        "sprint": {
          "sprints": [
            {"distance": "string", "time": "string", "rest": "string"}
          ]
        }
      }
    },

    "meals": [
      {
        "label": "string (e.g. breakfast, snack, lunch, dinner)",
        "time": "string (e.g. '8am')",
        "foods": [
          {"food": "string", "quantity": "string", "reference": ""}
        ]
      }
    ]
  },

  "examples": [
    {
      "instruction": "I did an intense 1-hour muscle training session this evening with bench press (8 and 11 reps at 60kg, 90 sec rest), then ate 200g of pasta and 2 eggs at 8pm.",
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
                {"reps": 8, "weight": "60kg", "rest": "90 sec"},
                {"reps": 11, "weight": "60kg", "rest": "90 sec"}
              ]
            }
          ]
        },
        "meals": [
          {
            "label": "dinner",
            "time": "8pm",
            "foods": [
              {"food": "pasta", "quantity": "200g"},
              {"food": "eggs", "quantity": "2"}
            ]
          }
        ]
      }
    },

    {
      "instruction": "This morning I did 3 sprints of 100m in 10s, 10s, and 11s with 5-minute rest between each.",
      "input": "",
      "output": {
        "activity": {
          "type": "sprint",
          "duration": "not specified",
          "intensity": "intense",
          "moment": "morning",
          "sprints": [
            {"distance": "100m", "time": "10s", "rest": "5min"},
            {"distance": "100m", "time": "10s", "rest": "5min"},
            {"distance": "100m", "time": "11s", "rest": "-"}
          ]
        },
        "meals": []
      }
    },

    {
      "instruction": "Quick breakfast with a bowl of Bjorg oatmeal and a banana at 8am.",
      "input": "",
      "output": {
        "activity": null,
        "meals": [
          {
            "label": "breakfast",
            "time": "8am",
            "foods": [
              {"food": "oatmeal", "quantity": "1 bowl", "reference": "Bjorg"},
              {"food": "banana", "quantity": "1"}
            ]
          }
        ]
      }
    }
  ]
}
```

--- 

### RAG DATA STRUCTURE
- All document chunks (from PDF, forum, articles) should be stored in a single file: rag_corpus.jsonl.
- Each line / sentence in the file is a chunk, containing:
  - the text (content)
  - the document source (source)
  - optional tags (tags) for filtering and semantic relevance

Example (rag_corpus.jsonl)

```json
{
  "content": "High-protein diets preserve lean mass during a cut.", 
  "source": "PubMed_1", 
  "tags": ["nutrition", "fat loss"]
}
{
  "content": "Carb cycling involves rotating high and low-carb days based on activity.", 
  "source": "Forum_Crossfit", 
  "tags": ["carbs", "timing", "training"]
}
{
  "content": "Crossfit improves fat oxidation when paired with moderate caloric deficit.", 
  "source": "Study_2023", 
  "tags": ["crossfit", "fat loss"]}
```

- These chunks will be indexed (e.g. using FAISS, Chroma, LlamaIndex) for retrieval based on similarity to the user’s input or profile.

---

### FINE-TUNING DATA STRUCTURE

- Fine-tuning is done using a separate file: fine_tune_dataset.jsonl.
- Each line is a complete training sample containing:
  - instruction: what the model should respond to 
  - input: optional additional context (can be empty)
  - output: the expected answer, structured or in plain text

Example (fine_tune_dataset.jsonl)
```json
{
  "instruction": "The user wants to lose fat and trains Crossfit 5x/week.",
  "input": "He eats a lot of carbs in the evening. How should he adjust his nutrition?",
  "output": "To lose fat while maintaining performance, reduce evening carbs and increase protein to 1.6–2.2g/kg body weight. Focus on whole foods, increase fiber intake, and distribute meals evenly throughout the day."
}
```
- The model will learn patterns, tone, and structure from these examples.
- It does not need to see the full scientific source, only the extracted and adapted recommendation.

---

#### DIRECTORY STRUCTURE 

 - data/ 
   - rag_corpus.jsonl (All semantic chunks for retrieval)
   - fine_tune_dataset.jsonl (Full prompts for fine-tuning)
   - sources/ (Raw original documents (PDF, TXT, etc.))
     - acsm_guidelines.pdf 
     - forum_crossfit.txt 
     - ...
- retriever/ (RAG system (indexing + search))
  - chunk_and_index.py 
  - query_retriever.py
- training/ 
  - fine_tune_config.yaml       # Axolotl config for QLoRA



---

CONCLUSION
- Use one file for RAG: merge all cleaned, chunked documents in rag_corpus.jsonl. 
- another file for fine-tuning: full instruction/response samples in fine_tune_dataset.jsonl. 
- Both systems are complementary: RAG injects factual, fresh knowledge; fine-tuning teaches structured reasoning and good output formatting.
