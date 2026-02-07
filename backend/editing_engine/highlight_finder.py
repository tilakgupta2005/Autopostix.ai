import dotenv
import os
import google.generativeai as genai
import json
import re

# --- Helper Function ---
def time_str_to_seconds(time_str):
    """Converts a HH:MM:SS time string to total seconds."""
    parts = list(map(int, time_str.split(':')))
    return parts[0] * 3600 + parts[1] * 60 + parts[2]

# --- Configuration ---
dotenv.load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --- Prompt ---
YOUR_PROMPT = """
## ROLE
You are an expert video editor's assistant.
## TASK
Analyze the provided transcript and select ONLY the most interesting, impactful, or highlight-worthy segments.
## CONSTRAINTS
- The total combined duration of the clips you select should be between 30 and 50 seconds.
- Each paragraph of the transcript is preceded by its time range in a 'startTime-endTime' format.
- The times are in seconds.
## OUTPUT FORMAT
- Return ONLY a single JSON array of objects.
- Do not add any explanation or markdown formatting around the JSON.
- Each object in the array must contain three keys: 'startTime' (string, "HH:MM:SS"), 'endTime' (string, "HH:MM:SS"), and 'transcript' (string).
"""

def FindHighlights(file_path):
    print(f"Finding Highlights")
    output_file_path = file_path.replace('.txt', '.json')
    try:
#read the transcript file
        print(f"Reading content from {file_path}...")
        with open(file_path, "r", encoding="utf-8") as file:
            file_content = file.read()
#gemini api call
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')
        full_prompt = f"{YOUR_PROMPT}\n\n---\n\n{file_content}"
        print("Sending request to Gemini...")
        response = model.generate_content(full_prompt)
#parse the response
        raw_text = response.text
        json_match = re.search(r'\[.*\]', raw_text, re.DOTALL)
        if not json_match:
            raise ValueError("No valid JSON array found in the response.")

        clean_json_str = json_match.group(0)
        final_clips = json.loads(clean_json_str)
        print("Successfully parsed highlight clips from Gemini.")

        total_duration = 0
        for clip in final_clips:
            start_seconds = time_str_to_seconds(clip['startTime'])
            end_seconds = time_str_to_seconds(clip['endTime'])
            total_duration += (end_seconds - start_seconds)

        print(f"--- Final Clips Selected by AI (Total Duration: {total_duration:.2f}s) ---")

        final_clips.sort(key=lambda x: time_str_to_seconds(x['startTime']))
        
        with open(output_file_path, "w", encoding="utf-8") as f:
            json.dump(final_clips, f, indent=2)
            
        print(f"Successfully saved the final clips to '{output_file_path}'")
        
        # Return the result for other potential uses
        return final_clips

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error parsing response from model: {e}. Raw response was:")
        print(globals().get('raw_text', 'Response not received.'))
        return None
    except KeyError as e:
        print(f"Error: The key '{e}' was not found in the JSON response.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    transcript_file = "temp/s01QuLpjISc/s01QuLpjISc.txt"
    highlight_data = FindHighlights(transcript_file)
    print(highlight_data)