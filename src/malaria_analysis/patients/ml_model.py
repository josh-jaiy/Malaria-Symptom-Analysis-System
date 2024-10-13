import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn.model_selection import train_test_split
from sklearn import metrics
import graphviz
from .models import Symptom, Patient  # Ensure the correct model import

# Function to prepare data and train the decision tree model
def train_decision_tree(patients_data):
    """
    Trains a decision tree classifier using patient data and symptoms. 
    The model predicts malaria type based on patient demographics and symptoms.
    """
    X = []
    y = []

    # Validate if there are patients to process
    if not patients_data.exists():
        raise ValueError("No patients data available for training.")

    # Get all symptoms from the Symptom model for binary encoding
    all_symptoms = Symptom.objects.all()
    symptom_names = [symptom.name for symptom in all_symptoms]

    if not symptom_names:
        raise ValueError("No symptom data found for encoding.")

    # Process each patient and extract features and labels
    for patient in patients_data:
        # Patient demographic data: Age and Gender
        features = [patient.age, 1 if patient.gender == 'Male' else 0]  # Encode gender (Male=1, Female=0)
        
        # Initialize a binary symptom vector
        symptom_vector = [0] * len(symptom_names)

        # Get patient's symptoms and encode them as a binary vector
        for symptom in patient.symptoms.all():
            if symptom.name in symptom_names:
                index = symptom_names.index(symptom.name)
                symptom_vector[index] = 1  # Mark presence of the symptom

        # Combine demographic data and symptom vector
        features.extend(symptom_vector)

        # Add the feature set to X and the malaria type to y (labels)
        X.append(features)
        y.append(patient.malaria_type)  # Label: malaria type

    # Convert lists to numpy arrays for processing
    X = np.array(X)
    y = np.array(y)

    # Handle case where there is insufficient data
    if len(X) < 2:
        raise ValueError("Insufficient patient data to train the model.")

    # Split data into training and test sets (80% train, 20% test)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train the Decision Tree Classifier
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train, y_train)

    # Make predictions on the test set
    y_pred = clf.predict(X_test)

    # Calculate and return the model's accuracy
    accuracy = metrics.accuracy_score(y_test, y_pred)

    return clf, accuracy

def visualize_tree(clf):
    """
    Generates a graphical visualization of the decision tree model and saves it as a file.
    """
    dot_data = export_graphviz(clf, out_file=None, 
                               feature_names=['Age', 'Gender'] + [symptom.name for symptom in Symptom.objects.all()],
                               class_names=['Malaria Type 1', 'Malaria Type 2', 'Malaria Type 3'],  # Adjust to actual classes
                               filled=True, rounded=True, 
                               special_characters=True)
    
    # Generate the tree graph
    graph = graphviz.Source(dot_data)
    graph_path = "media/plots/decision_tree"
    graph.render(graph_path)  # Save the graph to a file
    
    return graph_path  # Return the path where the tree is saved
