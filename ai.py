import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai
import os

# Set up the API key for Gemini API
API_KEY = "AIzaSyA0KZMs2xGI322pHG4FyXt11h_21-umkQI"
genai.configure(api_key=API_KEY)

# Memory file path
memory_file = 'mem.api'
policy_file = 'policy.api'  # Policy file path
message_history = []
policy = ""

# Function to load the last 10 messages from the memory file
def load_memory():
    global message_history
    if os.path.exists(memory_file):
        with open(memory_file, 'r') as f:
            content = f.read().strip()
            if content:
                message_history = content.split('\n\n')[-10:]

# Function to load the user-set policy from the policy file
def load_policy():
    global policy
    if os.path.exists(policy_file):
        with open(policy_file, 'r') as f:
            policy = f.read().strip()

# Function to save the current conversation to the memory file
def save_to_memory(user_input, gemini_response):
    global message_history
    # Add new message to history
    new_entry = f"User: {user_input}\nGemini: {gemini_response}"
    message_history.append(new_entry)
    
    # Keep only the last 10 messages
    if len(message_history) > 10:
        message_history = message_history[-10:]
    
    # Save to file
    with open(memory_file, 'w') as f:
        f.write('\n\n'.join(message_history))

# Function to get the response from Gemini API, including policy and context
def get_gemini_response():
    user_message = user_input.get("1.0", tk.END).strip()  # Get user input and remove extra spaces
    if not user_message:  # If the input is empty, do nothing
        return
    
    # Prepare context from the last 10 messages
    context = '\n\n'.join(message_history)
    
    # Combine policy, context, and user input for the prompt
    if policy:
        prompt = f"Policy:\n{policy}\n\nContext:\n{context}\n\nCurrent: {user_message}"
    else:
        prompt = f"Context:\n{context}\n\nCurrent: {user_message}"

    # Get response from the Gemini API
    response = model.generate_content(prompt)

    # Display the response in the result box
    result_box.config(state=tk.NORMAL)
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, response.text)
    result_box.config(state=tk.DISABLED)

    # Save the current conversation to memory
    save_to_memory(user_message, response.text)

    # Clear the input box after sending
    user_input.delete("1.0", tk.END)

# Initialize the main window
root = tk.Tk()
root.title("Gemini API Chat with Memory and Policy")
root.geometry("600x400")

# Dark mode colors
bg_color = "#1e1e1e"
fg_color = "#d4d4d4"
entry_bg = "#2d2d30"
button_bg = "#007acc"

root.configure(bg=bg_color)

# Create the input text box
user_input = tk.Text(root, height=5, bg=entry_bg, fg=fg_color, insertbackground="white", wrap=tk.WORD)
user_input.pack(padx=10, pady=10, fill=tk.BOTH)

# Create the response display box (read-only)
result_box = scrolledtext.ScrolledText(root, height=10, bg=entry_bg, fg=fg_color, wrap=tk.WORD)
result_box.pack(padx=10, pady=10, fill=tk.BOTH)
result_box.config(state=tk.DISABLED)

# Create the Send button
send_button = tk.Button(root, text="Send", bg=button_bg, fg="white", command=get_gemini_response)
send_button.pack(pady=10)

# Configure fonts and styles
user_input.config(font=("Arial", 12), relief=tk.FLAT)
result_box.config(font=("Arial", 12), relief=tk.FLAT)
send_button.config(font=("Arial", 12), relief=tk.FLAT)

# Create the model instance
model = genai.GenerativeModel("gemini-1.5-flash")

# Load the memory and policy when the app starts
load_memory()
load_policy()

# Run the app
root.mainloop()

