import requests
from bs4 import BeautifulSoup


def get_recipes(user_menu, user_allergies):

    host = 'https://eda.ru'
    url = 'https://eda.ru/recipesearch'
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}
    params = {'q': user_menu}

    instructions = []
    ingredients = []
    recipes = []

    global_response = requests.get(url, headers=headers, params=params)
    global_soup = BeautifulSoup(global_response.text, 'html.parser')
    global_items = global_soup.find_all('div', class_='tile-list__horizontal-tile horizontal-tile js-portions-count-parent js-bookmark__obj')

    for item in global_items:
        link = item.find('div', class_='clearfix').find('div', class_='horizontal-tile__content').find('h3', class_='horizontal-tile__item-title item-title').find('a').get('href')
        url = f'{host}{link}'
        recipe_response = requests.get(url, headers=headers)
        recipe_soup = BeautifulSoup(recipe_response.text, 'html.parser')

        instructions_html = recipe_soup.find_all('span', itemprop='text')
        for instruction_html in instructions_html:
            instruction = instruction_html.get_text()
            pure_instruction = instruction.replace('\xa0', ' ')
            instructions.append(pure_instruction )


        ingredients_html = recipe_soup.find_all('span', itemprop='recipeIngredient')
        for ingredient_html in ingredients_html:
            ingredient_quantity_html = ingredient_html.find_next('span').find_next('span')
            ingredient_quantity = ingredient_quantity_html.get_text()
            ingredient = ingredient_html.get_text()
            ingredients.append(
                {
                    ingredient: ingredient_quantity
                }
            )

        recipes.append(
            {
                'name': recipe_soup.find('meta', itemprop='keywords').get('content'),
                'photo_link': recipe_soup.find('span', itemprop='resultPhoto').get('content'),
                'calories': recipe_soup.find('span', itemprop='calories').get_text(),
                'ingredients': ingredients,
                'istructions': instructions
            }
        )

    return recipes




