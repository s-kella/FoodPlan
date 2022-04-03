import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError
from allergies import check_for_allergy, make_allergies_params


def get_image(url):
    response = requests.get(url)
    response.raise_for_status()
    photo = response.content
    return photo


def choose_menu(user_menu):
    if user_menu == 'Классическое':
        return ''
    if user_menu == 'Низкоуглеводное':
        return 'nizkokaloriynaya-eda'
    if user_menu == 'Вегетерианское':
        return 'vegetarianskaya-eda'
    if user_menu == 'Кето':
        return 'postnaya-eda'


def check_link(link):
    elements_quantity = 0
    for symbol in link:
        if symbol == '/':
            elements_quantity += 1
    if elements_quantity == 3:
        return True
    else:
        return False


def purify_links(links):
    purified_links = []
    for link in links:
        if link not in purified_links:
            purified_links.append(link)
    return purified_links


def get_recipes(user_menu, user_allergies, page):

    host = 'https://eda.ru'
    menu = choose_menu(user_menu)
    allergies = make_allergies_params(user_allergies)
    url = f'https://eda.ru/recepty/{menu}'
    params = {'page': page}
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'}

    links = []
    recipes = []

    global_response = requests.get(url, headers=headers, params=params)
    global_response.raise_for_status()
    global_soup = BeautifulSoup(global_response.text, 'html.parser')
    global_items = global_soup.find_all('a')

    for item in global_items:
        link = item.get('href')
        if check_link(link):
            links.append(link)

    purified_links = purify_links(links)

    for pure_link in purified_links:
        recipe_approved = True
        instructions = []
        ingredients_with_quantity = []
        ingredients = []

        url = f'{host}{pure_link}'
        recipe_response = requests.get(url, headers=headers)
        recipe_response.raise_for_status()
        recipe_soup = BeautifulSoup(recipe_response.text, 'html.parser')

        ingredients_html = recipe_soup.find_all('span', itemprop='recipeIngredient')

        for ingredient_html in ingredients_html:
            ingredient = ingredient_html.get_text()
            ingredient_quantity_html = ingredient_html.find_next('span').find_next('span')
            ingredient_quantity = ingredient_quantity_html.get_text()
            ingredients.append(ingredient)
            ingredients_with_quantity.append(
                {
                    ingredient: ingredient_quantity
                }
            )

        instructions_html = recipe_soup.find_all('span', itemprop='text')

        for instruction_html in instructions_html:
            instruction = instruction_html.get_text()
            pure_instruction = instruction.replace('\xa0', ' ')
            instructions.append(pure_instruction )

        for ingredient in ingredients:
            if not check_for_allergy(ingredient, allergies):
                recipe_approved = False
                break

        if recipe_approved:
            try:
                recipes.append(
                    {
                        'name': recipe_soup.find('meta', itemprop='keywords').get('content'),
                        'photo_link': recipe_soup.find('span', itemprop='resultPhoto').get('content'),
                        'calories': recipe_soup.find('span', itemprop='calories').get_text(),
                        'ingredients': ingredients_with_quantity,
                        'istructions': instructions
                    }
                )
            except AttributeError:
                pass

    return recipes


if __name__ == '__main__':

    recipes = []
    page = 1
    while (len(recipes) < 10):
        recipes += get_recipes(['Классическое'], ['Мясо'], page)
        page += 1

    for recipe in recipes:
        print(recipe)
