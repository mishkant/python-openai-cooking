# პროექტისთვის აუცილებელი ბიბლიოთეკების იმპორტი
import requests
import re
import shutil
import openai
from PIL import Image


# დარეგისტრირდით OpenAI-ზე და შექმენით გასაღები: API_KEY
openai.api_key = "YOUR_API_KEY"


# GPT(Generative Pre-trained Transformer)-სთვის შეკითხვის კონსტრუქციის შექმნა და ფუნქციაში განსაზღვრა
def create_dish_prompt(ingredients):
    prompt = f"Create a detailed recipe based on only the following ingredients: {', '.join(ingredients)}.\n"\
            + f"Additionally, assign a title starting with 'Recipe Title: ' to this dish, "\
            + f"which can be used to create a photorealistic image for it."
    
    return prompt


# ინგრედიენტების მიწოდება
products = ["strawberry", "cocoa", "cream", "dough"]


# Prompt-ის სრული კონსტრუქციის შექმნა
recipe_prompt = create_dish_prompt(products)


# კონსტრუირებული Prompt-ის გადაგზავნა OpenAI API-სთან
response = openai.Completion.create(engine = "text-davinci-003",
                                    prompt = recipe_prompt,
                                    max_tokens = 256,
                                    temperature = 0.7)

# OpenAI-ს პასუხის დამუშავება და ეკრანზე გამოტანა
recipe = response["choices"][0]["text"]
print(recipe)


# მიღებული პასუხიდან რეცეპტის სათაურის ამოღება
def extract_title(recipe):
    return re.findall("^.*Recipe Title: .*$", recipe, re.MULTILINE)[0].strip().split("Recipe Title: ")[1]

print(extract_title(recipe))


# DALLE-E მოდელისთვის prompt-ის კონსტრუირება მიღებული რეცეპრის სათაურის გამოყენებით
def dalle2_prompt(recipe_title):
    prompt = f"'{recipe_title}', professional food photography, 15mm, studio lighting."
    
    return prompt

image_prompt = dalle2_prompt(extract_title(recipe))


# DALLE-E მოდელში კონსტრუირებული prompt-ის გადაგზავნა
response = openai.Image.create(prompt = image_prompt,
                               n = 1,
                               size = "1024x1024")

# მიღებული ვიზუალური ობიექტის ადგილმდებარეობის/ლინკის ამოღება
image_url = response['data'][0]['url']
print(image_url)


# მიღებული ვიზუალური ობიექტის ლინკიდან სურათის ლოკალურად ჩამოწერა
def save_image(image_url, file_name):
    image_res = requests.get(image_url, stream = True)
    
    if image_res.status_code == 200:
        with open(file_name,'wb') as f:
            shutil.copyfileobj(image_res.raw, f)
    else:
        print("Error downloading image!")
        
    return image_res.status_code

save_image(image_url, "my_recipe.png")


# ჩამოწერილი სურათის დაბეჭდვა (Jupyter-ში, ან ნახეთ სურათი საქაღალდეში)
Image.open("my_recipe.png")
