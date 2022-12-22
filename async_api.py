# aiohttp is the equivalent to requests, but async
import aiohttp

# Required for async I/O
import asyncio

MINDAT_API_URL = "https://api.mindat.org"
YOUR_API_KEY = ""       # you need to fill this in

# Where to get an API key:
# 1) Log in to Mindat.org, you need an authenticated account (ask Jolyon!)
# 2) go to "My homepage"->"Edit my page"
# 3) At the bottom of the page you will find "API Key - Your key:"
# *  best practice is not use API KEY directly in code,
#    but store them in ENV variables, or files outside the project directory

headers = {'Authorization': 'Token '+YOUR_API_KEY, 'Accept':'application/json'}

async def main():
    s = aiohttp.ClientSession(headers=headers)

    # https://api.mindat.org/items/?format=json
    # return all mindat items (minerals, varieties, groups, synonyms, rocks, etc.),
    # unfiltered, paginated

    # Sending GET HTTP request with specified header & parameters
    response = await s.get(MINDAT_API_URL+"/items/")

    print(response)                            #Expected output: >>>  <Response [200]>
    print(await response.json())

    # https://api.mindat.org/items/?fields=id,name,dispformulasimple&page_size=100
    # display only selected fields.
    # selecting only necessary fields slightly reduces db queries size so its appreciated
    # customize page_size to 100 items per page
    params = {'fields': 'id,name,dispformulasimple',
            'page_size': '100'}

    r = await s.get(MINDAT_API_URL+"/items/", params=params)

    # https://api.mindat.org/items/?omit=id,name,dispformulasimple
    # exclude fields from display
    params = {'omit': 'id,name,dispformulasimple',
            'format': 'json'}

    # filters on minerals, examples
    # https://api.mindat.org/items/?density__to=3&crystal_system=Triclinic&color=red&ima=1
    params = {'density__to': '3',
            'crystal_system': 'Triclinic',
            'color': 'red',
            'ima': 1}          # show only minerals approved by ima}
    r = await s.get(MINDAT_API_URL+"/items/", params=params)

    print(r)                            #Expected output: >>>  <Response [200]>
    print(await r.json())


    # for filters reference on this endpoint see generated documentation:
    # https://api.mindat.org/schema/redoc/#tag/items/operation/items_list

    # https://api.mindat.org/items/?updated_at=2022-10-30
    # Allows taking only changed records, if someone is syncronizing his db with mindat.
    #Last updated datetime in format %Y-%m-%d %H:%M:%S:

    # fields that display relations to other items are:
    # groupid - Group id  e.g. Tourmaline group => Elbaite
    # variety of - Variety of, e.g. Quartz => Amethyst
    # synid - Synonym id
    # relations - other relations between items
    # ! to enable relations field in items output add parameter:
    # https://api.mindat.org/items/?expand=relations
    params = {'expand': 'relations'}
    r = await s.get(MINDAT_API_URL+"/items/", params=params)


    # To list localities, where the mineral/item is present,
    # add 'expand=localities' query parameter
    # https://api.mindat.org/items/?expand=localities&fields=id,name,localities


    # https://api.mindat.org/items/{id}/varieties/
    # special endpoint that returns all varieties of an item (mineral), recursively, e.g. Quartz => Chalcedony => Agate
    # e.g., all varieties of Quartz (except parent, quartz itself):
    # https://api.mindat.org/items/3337/varieties/?fields=id,name,varietyof&page_size=1000
    params = {'fields': 'id,name,varietyof',
            'page_size': '1000'}
    r = await s.get(MINDAT_API_URL+"/items/3337/varieties/",
                    params=params)


    # https://api.mindat.org/items_search/?q=raelgard
    # Endpoint that exactly copies the algorithm of fuzzy search for mineral name on mindat,
    # returning results of fuzzy search
    #        Returns minerals where name contains search term.
    #        If they are not found, returns names with the least levenshtein distance
    #        Query parameters:
    #           q (search term),
    #           size (number of returned records, applicable only for levenshtein search results, default 12)
    params = {'q': 'raelgard'}
    r = await s.get(MINDAT_API_URL+"/items_search/",
                    params=params)


    # https://api.mindat.org/minerals_ima/
    # Endpoint returning IMA related data and IMA-approved minerals only
    r = s.get(MINDAT_API_URL+"/minerals_ima/")

    print(r)                            #Expected output: >>>  <Response [200]>
    print(await r.json())


    # https://api.mindat.org/localities/?id__in=&updated_at=&elements_inc=&elements_exc=&txt=Belorech&description=&country=
    # Localities endpoint

    # To list locality's minerals, where the mineral/item is present,
    # add 'expand=items' query parameter
    # https://api.mindat.org/localities/?expand=items&fields=id,name,items
    params = {'expand': 'items',
            'fields': 'id,name,items'}
    r = await s.get(MINDAT_API_URL+"/minerals_ima/",
                    params=params)


    # There is automatically generated documentation for MindatAPI in OpenAPI3 format:
    # https://api.mindat.org/schema/redoc
    # it is in beta and many descriptions are not comlete.

if __name__ == '__main__':
    asyncio.run(main())