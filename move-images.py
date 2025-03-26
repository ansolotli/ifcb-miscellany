import os
import shutil

extracted_images_folder = "D:/IFCB/data/extracted-images-cyanobacteria-2024/extracted-images-cyanobacteria-2024"
output_folder = "D:/IFCB/data/2024-summer-cyanobacteria-images"

def combine_days(extracted_images_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    day_counter = 1
    
    # Loop over each day folder in the base folder
    for day_folder in os.listdir(extracted_images_folder):
        day_folder_path = os.path.join(extracted_images_folder, day_folder)

        # Loop over each species folder within the day folder
        for species_folder in os.listdir(day_folder_path):
            species_folder_path = os.path.join(day_folder_path, species_folder)
            
            # Create the species folder in the output directory if it doesn't exist
            output_species_folder = os.path.join(output_folder, species_folder)
            os.makedirs(output_species_folder, exist_ok=True)
            
            # Copy each image from the current species folder to the output species folder
            for image in os.listdir(species_folder_path):
                image_file = os.path.join(species_folder_path, image)
                
                # Ensure you only copy files (not subdirectories)
                if os.path.isfile(image_file):
                    output_file = os.path.join(output_species_folder, image)

                    shutil.copy2(image_file, output_file)
        print(f"ok, that was day number {day_counter}")
        day_counter = day_counter + 1

    print("Done!")

combine_days(extracted_images_folder, output_folder)