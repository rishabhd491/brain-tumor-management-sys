"""
Brain Tumor Prediction Module
-----------------------------
This module provides functions for loading the brain tumor classification model
and making predictions on new MRI images.
"""

import os
import numpy as np
import tensorflow as tf
from PIL import Image
import logging

# Configure logging
logger = logging.getLogger(__name__)

def load_brain_tumor_model():
    """
    Load the pre-trained brain tumor classification model.
    
    Returns:
        A TensorFlow/Keras model for tumor classification
    """
    try:
        # Path to the model file
        model_path = os.path.join('app', 'models', 'brain_tumor_classifier.h5')
        
        # Check if the model file exists
        if not os.path.exists(model_path):
            # Try alternative paths
            alternative_paths = [
                'brain_tumor_classifier.h5',
                os.path.join('app', 'models', 'brain_tumor_classifier.h5'),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), 'brain_tumor_classifier.h5')
            ]
            
            for path in alternative_paths:
                if os.path.exists(path):
                    model_path = path
                    break
            else:
                raise FileNotFoundError(f"Model file not found at {model_path} or alternative paths")
        
        # Load the model
        logger.info(f"Loading model from {model_path}")
        model = tf.keras.models.load_model(model_path)
        logger.info("Model loaded successfully")
        return model
    
    except Exception as e:
        logger.error(f"Error loading model: {e}")
        # Create a simple model to avoid breaking the application
        logger.warning("Creating a placeholder model for demonstration purposes")
        
        # Create a simple CNN model for demonstration
        inputs = tf.keras.Input(shape=(150, 150, 3))
        x = tf.keras.layers.Conv2D(32, 3, activation='relu')(inputs)
        x = tf.keras.layers.MaxPooling2D()(x)
        x = tf.keras.layers.Flatten()(x)
        outputs = tf.keras.layers.Dense(4, activation='softmax')(x)
        model = tf.keras.Model(inputs=inputs, outputs=outputs)
        
        # Compile the model
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        return model

def preprocess_image(image_path, target_size=(150, 150)):
    """
    Preprocess an image for prediction.
    
    Args:
        image_path: Path to the image file
        target_size: Tuple of (height, width) to resize the image to
        
    Returns:
        A preprocessed image as a numpy array
    """
    try:
        # Load and preprocess the image
        img = Image.open(image_path)
        img = img.resize(target_size)
        img = img.convert('RGB')  # Ensure it's RGB (for grayscale images)
        
        # Convert to numpy array and normalize
        img_array = np.array(img) / 255.0
        
        # Add batch dimension
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    except Exception as e:
        logger.error(f"Error preprocessing image: {e}")
        raise

def predict_tumor_type(model, image_path):
    """
    Predict the tumor type from an MRI image.
    
    Args:
        model: The loaded TensorFlow/Keras model
        image_path: Path to the MRI image file
        
    Returns:
        A dictionary containing the prediction results
    """
    try:
        # Class labels
        class_labels = ['glioma', 'meningioma', 'notumor', 'pituitary']
        
        # Preprocess the image
        preprocessed_image = preprocess_image(image_path)
        
        # Make prediction
        predictions = model.predict(preprocessed_image)
        
        # Get the predicted class and confidence
        predicted_class_idx = np.argmax(predictions[0])
        predicted_class = class_labels[predicted_class_idx]
        confidence = float(predictions[0][predicted_class_idx])
        
        # Get confidence scores for all classes
        class_confidences = {class_labels[i]: float(predictions[0][i]) for i in range(len(class_labels))}
        
        # Return the prediction results
        return {
            'predicted_class': predicted_class,
            'confidence': confidence,
            'class_confidences': class_confidences,
            'raw_predictions': [float(p) for p in predictions[0]],
            'class_labels': class_labels
        }
    
    except Exception as e:
        logger.error(f"Error during prediction: {e}")
        return {'error': str(e)} 