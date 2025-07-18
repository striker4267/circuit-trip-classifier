import torch
from transformers import pipeline
import pandas as pd
import math
import os

# Check for CUDA availability and set device_id for GPU or CPU
if torch.cuda.is_available():
    print(f"CUDA is available. Using GPU: {torch.cuda.get_device_name(0)}")
    device_id = 0 # Use GPU (device 0)
else:
    print ("CUDA is not available. Using CPU")
    device_id = -1 # Use CPU

# Initialize English to French translation pipeline using the specified model and device
translator_en_fr = pipeline(
    "translation",
    model = "Helsinki-NLP/opus-mt-en-fr",
    device= device_id
)

# Initialize French to English translation pipeline using the specified model and device
translator_fr_en = pipeline(
    "translation", 
    model= "Helsinki-NLP/opus-mt-fr-en",
    device = device_id
)

def translate(cause_csv, action_csv, cause_types_csv, combined_csv):
    """
    Orchestrates the back-translation process for low-frequency text categories.
    It manages execution flags, loads data, augments, and saves results.
    """
    # Check if the process has already fully completed in a previous run
    if not os.path.exists("data/back_translation_has_run.flag"):
        print("Running back-translation process...")

        # Create a temporary flag file if it does not exist to track progress
        if not os.path.exists("data/back_translation_temp.flag"):
            with open("data/back_translation_temp.flag", "w") as f:
                f.write("0") # Initialize progress to 0 (meaning no categories processed yet)

    else:
        print("Already back translated before, skipping.")
        return # Exit if the process has already successfully completed
    
    # Load input data from CSV files
    # df_c contains cause information
    df_c = pd.read_csv(cause_csv)
    # df_a contains action (description) text
    df_a = pd.read_csv(action_csv)
    # df_ct contains categories and their frequencies (counts)
    df_ct = pd.read_csv(cause_types_csv) 

    count = 1 # Initialize counter for current category being processed (for flag tracking)
    
    # Iterate through each cause (category) and its frequency from the cause_types_csv
    for cause, frequency in df_ct.itertuples(index=False):
        print(f"\n--- Processing Category: '{cause}' (Original Frequency: {frequency}) ---")

        # Read progress from the temporary flag file
        # If the current category's count is <= the saved progress, skip it (already processed)
        with open("data/back_translation_temp.flag", 'r') as f:
            if int(f.read()) >= count:
                print(f"Skipping '{cause}', already processed in a previous run.")
                count +=1 # Increment counter for the next potential processing
                continue # Skip to the next cause

        # --- Augmentation Logic for Frequencies < 400 and > 100 ---
        # (This block targets categories for moderate augmentation)
        if frequency < 400 and frequency > 100:
            # Determine multiplication factor based on frequency to reach target (800 or 1000)
            if frequency > 250:
                factor = math.ceil(1000/frequency)
            else:
                factor = math.ceil(800/ frequency)
            
            print(f"  Strategy: Moderate Augmentation (Target Factor: {factor})")

            # Get original sentences for the current cause
            # Assumes 'Cause' column in df_c aligns with 'Action' in df_a by index
            indexes = df_c.index[df_c['Cause'] == cause].tolist()
            sentences = df_a.loc[indexes, 'Action'].tolist()
            if len(sentences) == 0:
                print(f"  Warning: No original sentences found for cause: '{cause}'. Skipping augmentation.")
                count += 1
                continue # Skip if no sentences found for this cause
            
            print(f"  Original sentences count: {len(sentences)}")

            mod_sentences = sentences.copy() # Start with original sentences

            # Augment by repeatedly translating the original sentences
            # This loop will run (factor - 1) times, adding (factor - 1) copies of translated originals
            # Total sentences will be original_count + (original_count * (factor - 1)) = original_count * factor
            for i in range(factor - 1):
                print(f"  Augmenting originals - round {i+1}/{factor-1} (current total: {len(mod_sentences)})")
                mod_sentences.extend(batch_translator(sentences))
            
            # Note: This strategy prioritizes original data quality over maximum diversity
            # by repeatedly re-translating only the 'sentences' (originals).


        # --- Augmentation Logic for Frequencies < 100 ---
        # (This block targets categories for more aggressive augmentation)
        elif frequency <= 100:
            # Determine multiplication factor and 'max' rounds for initial diversity
            if frequency > 80:
                max = 1
                factor = math.ceil( (600/ frequency)/max)
            elif frequency > 50:
                max = 2
                factor = math.ceil( (500/ frequency)/max)
            else:
                max = 3
                factor = math.ceil( (300/ frequency)/max)
            
            print(f"  Strategy: Aggressive Augmentation (Diversity Rounds: {max}, Total Factor: {factor})")

            # Get original sentences for the current cause
            # Assumes 'Cause' column in df_c aligns with 'Action' in df_a by index
            indexes = df_c.index[df_c['Cause'] == cause].tolist()
            sentences = df_a.loc[indexes, 'Action'].tolist()
            if len(sentences) == 0:
                print(f"  Warning: No original sentences found for cause: '{cause}'. Skipping augmentation.")
                count += 1
                continue # Skip if no sentences found for this cause
            
            print(f"  Original sentences count: {len(sentences)}")


            augmented = sentences.copy() # Start with original sentences for initial augmentation

            # First phase: Build diversity by translating ORIGINAL sentences multiple times
            # This creates: original + (max rounds of back-translated originals)
            for round_num in range(max):
                print(f"  Phase 1 (Diversity): '{cause}' - round {round_num+1}/{max} (current total: {len(augmented)})")
                augmented.extend(batch_translator(sentences))  # Always translate originals

            print(f"  After Phase 1 (Diversity Building): {len(sentences)} originals -> {len(augmented)} sentences")

            mod_sentences = augmented.copy() # Start 'mod_sentences' with the diverse 'augmented' set
            
            # Second phase: Scale up by back-translating the entire augmented set
            # This loop runs (factor - max) times, from 'max' up to 'factor' (exclusive)
            for round_num in range(max, factor): 
                print(f"  Phase 2 (Scaling): '{cause}' - round {round_num+1-max}/{factor-max} (current total: {len(mod_sentences)})")
                mod_sentences.extend(batch_translator(augmented))
        else:
            print(f"  Strategy: No Augmentation (Frequency {frequency} is >= 400)")
            # Get original sentences for the current cause
            indexes = df_c.index[df_c['Cause'] == cause].tolist()
            sentences = df_a.loc[indexes, 'Action'].tolist()
            # No augmentation, so mod_sentences is just a copy of the originals
            mod_sentences = sentences.copy()
            if len(sentences) == 0:
                print(f"  Warning: No original sentences found for cause: '{cause}'. Skipping.")
                count += 1
                continue

        print(f"Final augmented count for '{cause}': {len(sentences)} originals -> {len(mod_sentences)} total sentences.")
        # Append the (original + augmented) sentences for the current cause to the combined CSV
        # Data is saved per category for robust recovery in case of interruption.
        append_sentences_to_csv(mod_sentences, cause, combined_csv )
        print(f"Appended '{cause}' data to '{combined_csv}'.")

        # Update the temporary flag with the count of the just-processed category
        with open("data/back_translation_temp.flag", "w") as f:
            f.write(str(count))
        count +=1 # Increment counter for the next category


    # Rename the temporary flag to indicate full completion of the entire process
    os.rename("data/back_translation_temp.flag", "data/back_translation_has_run.flag")
    print("\nBack-translation process completed successfully!")


def batch_translator(texts, batch_size = 16):
    """
    Performs back-translation (EN->FR->EN) on a list of texts in batches.
    """
    results = [] # To store all back-translated sentences

    # Process texts in batches for efficiency
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        # print(f"  Translating batch {i//batch_size + 1} of {math.ceil(len(texts)/batch_size)}") # Optional: very verbose

        # Translate batch from English to French
        fr_results = translator_en_fr(batch)
        fr_text = [res['translation_text'] for res in fr_results]

        # Translate batch from French back to English
        en_results = translator_fr_en(fr_text)
        en_text = [res['translation_text'] for res in en_results]
        
        results.extend(en_text) # Add translated sentences to the results list
    return results


def append_sentences_to_csv(sentences, cause, combined_csv ):
    """
    Creates a DataFrame from augmented sentences for a single cause and appends it to a CSV.
    """
    df_new = pd.DataFrame({
        'Cause': [cause] * len(sentences), # Assign the cause label to all sentences
        'Action': sentences # The list of sentences
    })
    # Append to CSV: mode='a' (append), header=False (don't write header again), index=False (don't write DataFrame index)
    df_new.to_csv(combined_csv, mode= 'a', header=False, index=False)
