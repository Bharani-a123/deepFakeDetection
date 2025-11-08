import numpy as np
from PIL import Image
from your_model_script import classify_image  # replace with actual script name where function is defined

# Load your sample image using PIL
image_path = "obc.jpg"
image = Image.open(image_path)

# Convert to numpy array if needed
image_np = np.array(image)

# Call the classifier
result = classify_image(image_np)

print("Deepfake Detection Result:", result)
