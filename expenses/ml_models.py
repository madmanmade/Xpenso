import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import joblib
import os
from django.conf import settings

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')

class ExpenseCategoryPredictor:
    def __init__(self):
        self.model = None
        self.label_encoder = LabelEncoder()
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        
    def preprocess_text(self, text):
        # Convert to lowercase
        text = str(text).lower()
        
        # Remove special characters and numbers
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens if token not in self.stop_words]
        
        return ' '.join(tokens)
    
    def train(self, data_path):
        # Load data
        df = pd.read_csv(data_path)
        
        # Preprocess descriptions
        df['processed_description'] = df['description'].apply(self.preprocess_text)
        
        # Encode categories
        self.label_encoder.fit(df['category'])
        y = self.label_encoder.transform(df['category'])
        
        # Create and train pipeline
        self.model = Pipeline([
            ('tfidf', TfidfVectorizer(
                ngram_range=(1, 2),
                max_features=5000,
                min_df=2
            )),
            ('classifier', RandomForestClassifier(
                n_estimators=200,
                max_depth=None,
                min_samples_split=2,
                min_samples_leaf=1,
                class_weight='balanced',
                random_state=42
            ))
        ])
        
        # Train the model
        self.model.fit(df['processed_description'], y)
        
    def predict(self, description):
        # Preprocess input description
        processed_description = self.preprocess_text(description)
        
        # Make prediction
        prediction = self.model.predict([processed_description])[0]
        
        # Return predicted category
        return self.label_encoder.inverse_transform([prediction])[0]
    
    def predict_proba(self, description):
        # Preprocess input description
        processed_description = self.preprocess_text(description)
        
        # Get probability predictions
        probas = self.model.predict_proba([processed_description])[0]
        
        # Get top 3 predictions with their probabilities
        top_indices = np.argsort(probas)[-3:][::-1]
        
        predictions = []
        for idx in top_indices:
            category = self.label_encoder.inverse_transform([idx])[0]
            probability = probas[idx]
            predictions.append((category, probability))
        
        return predictions
    
    def save_model(self, path):
        """Save the trained model to disk"""
        model_data = {
            'model': self.model,
            'label_encoder': self.label_encoder
        }
        joblib.dump(model_data, path)
    
    def load_model(self, path):
        """Load a trained model from disk"""
        model_data = joblib.load(path)
        self.model = model_data['model']
        self.label_encoder = model_data['label_encoder']

def train_and_save_model():
    """Utility function to train and save the model"""
    predictor = ExpenseCategoryPredictor()
    data_path = os.path.join(settings.BASE_DIR, 'dataset.csv')
    model_path = os.path.join(settings.BASE_DIR, 'expenses', 'trained_model.joblib')
    
    predictor.train(data_path)
    predictor.save_model(model_path)
    return predictor

if __name__ == "__main__":
    # Train and save the model
    predictor = train_and_save_model()
    
    # Test the model with some sample expenses
    test_expenses = [
        "Grocery shopping at Walmart",
        "Monthly rent payment",
        "Netflix subscription",
        "Gas station fill up",
        "Restaurant dinner"
    ]
    
    print("\nTesting expense category predictions:")
    print("-" * 50)
    for expense in test_expenses:
        prediction = predictor.predict(expense)
        probas = predictor.predict_proba(expense)
        
        print(f"\nExpense: {expense}")
        print(f"Predicted category: {prediction}")
        print("Top 3 predictions with probabilities:")
        for category, prob in probas:
            print(f"  {category}: {prob:.2%}")