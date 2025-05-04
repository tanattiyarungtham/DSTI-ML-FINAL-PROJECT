The NLP Fitness Assistance model is built to guide users on their fitness journey using everyday language. Using Hugging Face Transformers, it brings together intent detection, calorie calculation, and personalized AI-driven fitness advice.

The app focuses on three main tasks: figuring out what the user wants to do (like logging progress, planning weight changes, or asking for advice), calculating nutritional needs, and giving health-related recommendations.

Users can simply type in their goals or questions. If they’re sharing a log, the app saves it. If they want to lose or gain weight, it calculates things like BMR, TDEE, and daily calorie adjustments required to achieve the provided weight management goal. And if they’re looking for general advice, a fine-tuned language model provides useful responses.

For intent detection, the app uses a BERT model trained on a custom dataset with three categories. For workout advice, it uses the Soorya03/Llama-3.2-1B-Instruct-FitnessAssistant model. Calorie calculations are handled by a custom function that extracts information from the user’s text and applies health formulas. For future development, each user’s profile will be stored in a log file for easy tracking.

To get started, install the required packages listed in requirements.txt and run the script in a Python environment. You’ll also need a CSV file named intent\_data\_ad\_log\_pro.csv with labeled examples to train the intent model. After that, you can enter something like "I'm a 29-year-old woman, 56 kg, 163 cm, moderately active. I want to lose 2 kg in 2 months," and get a clear, personalized response.

The current version focuses entirely on direct text input. A chatbot interface will be implemented in the near future.

Model Notebook:

notebooks / Fitness_Assistance_model.ipynb

Libraries and tools used:

- Transformers (Hugging Face)
- Datasets (Hugging Face)
- Scikit-learn
- Torch (PyTorch)
- Pandas
- NumPy
- Regex (for input parsing)

Model:

- Soorya03/Llama-3.2-1B-Instruct-FitnessAssistant (for advice generation)
- Fine-tuned BERT (for intent detection)

Data source:

- Custom-labeled intent dataset in CSV format named intent\_data\_ad\_log\_pro.csv

This project combines natural language understanding with structured health advice and sets the foundation for a more interactive assistant in future development stages.
