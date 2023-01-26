import fastdup
fastdup.run("/Users/liorrozin/Desktop/2.0")
fastdup.create_duplicates_gallery('similarity.csv',save_path='.', num_images=20, max_width=400)
from IPython.display import HTML
HTML('similarity.html')
print("Done")