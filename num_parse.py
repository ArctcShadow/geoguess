import json
import time
from geopy.geocoders import Nominatim

detailed_codes = {
    # Alabama
    "205": "Birmingham, Alabama", "251": "Mobile, Alabama", "256": "Huntsville, Alabama", 
    "334": "Montgomery, Alabama", "659": "Birmingham, Alabama", "938": "Huntsville, Alabama",
    
    # Alaska
    "907": "Anchorage, Alaska",
    
    # Arizona
    "480": "Mesa, Arizona", "520": "Tucson, Arizona", "602": "Phoenix, Arizona", 
    "623": "Glendale, Arizona", "928": "Flagstaff, Arizona",
    
    # Arkansas
    "327": "Little Rock, Arkansas", "479": "Fayetteville, Arkansas", "501": "Little Rock, Arkansas", "870": "Jonesboro, Arkansas",
    
    # California
    "209": "Stockton, California", "213": "Los Angeles, California", "279": "Sacramento, California",
    "310": "Los Angeles, California", "323": "Los Angeles, California", "341": "Oakland, California",
    "350": "Stockton, California", "369": "Vallejo, California", "408": "San Jose, California",
    "415": "San Francisco, California", "424": "Los Angeles, California", "442": "Oceanside, California",
    "510": "Oakland, California", "530": "Redding, California", "559": "Fresno, California",
    "562": "Long Beach, California", "619": "San Diego, California", "626": "Pasadena, California",
    "628": "San Francisco, California", "650": "San Mateo, California", "657": "Anaheim, California",
    "661": "Bakersfield, California", "669": "San Jose, California", "707": "Santa Rosa, California",
    "714": "Anaheim, California", "747": "San Fernando, California", "760": "Oceanside, California",
    "805": "Santa Barbara, California", "818": "San Fernando, California", "820": "Santa Barbara, California",
    "831": "Salinas, California", "840": "San Bernardino, California", "858": "San Diego, California",
    "909": "San Bernardino, California", "916": "Sacramento, California", "925": "Concord, California",
    "949": "Irvine, California", "951": "Riverside, California",
    
    # Colorado
    "303": "Denver, Colorado", "719": "Colorado Springs, Colorado", "720": "Denver, Colorado",
    "970": "Fort Collins, Colorado", "983": "Denver, Colorado",
    
    # Connecticut
    "203": "Bridgeport, Connecticut", "475": "Bridgeport, Connecticut", 
    "860": "Hartford, Connecticut", "959": "Hartford, Connecticut",
    
    # Delaware
    "302": "Wilmington, Delaware",
    
    # Florida
    "239": "Fort Myers, Florida", "305": "Miami, Florida", "321": "Orlando, Florida",
    "324": "Jacksonville, Florida", "352": "Gainesville, Florida", "386": "Daytona Beach, Florida",
    "407": "Orlando, Florida", "448": "Pensacola, Florida", "561": "West Palm Beach, Florida",
    "645": "Miami, Florida", "656": "Tampa, Florida", "689": "Orlando, Florida",
    "727": "St. Petersburg, Florida", "728": "West Palm Beach, Florida", "754": "Fort Lauderdale, Florida",
    "772": "Port St. Lucie, Florida", "786": "Miami, Florida", "813": "Tampa, Florida",
    "850": "Tallahassee, Florida", "863": "Lakeland, Florida", "904": "Jacksonville, Florida",
    "941": "Sarasota, Florida", "954": "Fort Lauderdale, Florida",
    
    # Georgia
    "229": "Albany, Georgia", "404": "Atlanta, Georgia", "470": "Atlanta, Georgia",
    "478": "Macon, Georgia", "678": "Atlanta, Georgia", "706": "Augusta, Georgia",
    "762": "Augusta, Georgia", "770": "Atlanta, Georgia", "912": "Savannah, Georgia", "943": "Atlanta, Georgia",
    
    # Hawaii
    "808": "Honolulu, Hawaii",
    
    # Idaho
    "208": "Boise, Idaho", "986": "Boise, Idaho",
    
    # Illinois
    "217": "Springfield, Illinois", "224": "Elgin, Illinois", "309": "Peoria, Illinois",
    "312": "Chicago, Illinois", "331": "Aurora, Illinois", "447": "Springfield, Illinois",
    "464": "Chicago, Illinois", "618": "Belleville, Illinois", "630": "Aurora, Illinois",
    "708": "Cicero, Illinois", "730": "Peoria, Illinois", "773": "Chicago, Illinois",
    "779": "Rockford, Illinois", "815": "Rockford, Illinois", "847": "Elgin, Illinois",
    "861": "Bloomington, Illinois", "872": "Chicago, Illinois",
    
    # Indiana
    "219": "Gary, Indiana", "260": "Fort Wayne, Indiana", "317": "Indianapolis, Indiana",
    "463": "Indianapolis, Indiana", "574": "South Bend, Indiana", "765": "Lafayette, Indiana",
    "812": "Evansville, Indiana", "930": "Evansville, Indiana",
    
    # Iowa
    "319": "Cedar Rapids, Iowa", "515": "Des Moines, Iowa", "563": "Davenport, Iowa",
    "641": "Mason City, Iowa", "712": "Sioux City, Iowa",
    
    # Kansas
    "316": "Wichita, Kansas", "620": "Dodge City, Kansas", "785": "Topeka, Kansas", "913": "Kansas City, Kansas",
    
    # Kentucky
    "270": "Bowling Green, Kentucky", "364": "Bowling Green, Kentucky", "502": "Louisville, Kentucky",
    "606": "Ashland, Kentucky", "859": "Lexington, Kentucky",
    
    # Louisiana
    "225": "Baton Rouge, Louisiana", "318": "Shreveport, Louisiana", "337": "Lafayette, Louisiana",
    "504": "New Orleans, Louisiana", "985": "Houma, Louisiana",
    
    # Maine
    "207": "Portland, Maine",
    
    # Maryland
    "227": "Silver Spring, Maryland", "240": "Silver Spring, Maryland", "301": "Silver Spring, Maryland",
    "410": "Baltimore, Maryland", "443": "Baltimore, Maryland", "667": "Baltimore, Maryland",
    
    # Massachusetts
    "339": "Boston, Massachusetts", "351": "Lowell, Massachusetts", "413": "Springfield, Massachusetts",
    "508": "Worcester, Massachusetts", "617": "Boston, Massachusetts", "774": "Worcester, Massachusetts",
    "781": "Boston, Massachusetts", "857": "Boston, Massachusetts", "978": "Lowell, Massachusetts",
    
    # Michigan
    "231": "Muskegon, Michigan", "248": "Troy, Michigan", "269": "Kalamazoo, Michigan",
    "313": "Detroit, Michigan", "517": "Lansing, Michigan", "586": "Warren, Michigan",
    "616": "Grand Rapids, Michigan", "734": "Ann Arbor, Michigan", "810": "Flint, Michigan",
    "906": "Marquette, Michigan", "947": "Troy, Michigan", "989": "Saginaw, Michigan",
    
    # Minnesota
    "218": "Duluth, Minnesota", "320": "St. Cloud, Minnesota", "507": "Rochester, Minnesota",
    "612": "Minneapolis, Minnesota", "651": "St. Paul, Minnesota", "763": "Brooklyn Park, Minnesota",
    "952": "Bloomington, Minnesota",
    
    # Mississippi
    "228": "Gulfport, Mississippi", "601": "Jackson, Mississippi", "662": "Tupelo, Mississippi", "769": "Jackson, Mississippi",
    
    # Missouri
    "235": "Rolla, Missouri", "314": "St. Louis, Missouri", "417": "Springfield, Missouri",
    "557": "St. Louis, Missouri", "573": "Columbia, Missouri", "636": "St. Charles, Missouri",
    "660": "Sedalia, Missouri", "816": "Kansas City, Missouri", "975": "Kansas City, Missouri",
    
    # Montana
    "406": "Billings, Montana",
    
    # Nebraska
    "308": "Grand Island, Nebraska", "402": "Omaha, Nebraska", "531": "Omaha, Nebraska",
    
    # Nevada
    "702": "Las Vegas, Nevada", "725": "Las Vegas, Nevada", "775": "Reno, Nevada",
    
    # New Hampshire
    "603": "Manchester, New Hampshire",
    
    # New Jersey
    "201": "Jersey City, New Jersey", "551": "Jersey City, New Jersey", "609": "Trenton, New Jersey",
    "640": "Trenton, New Jersey", "732": "New Brunswick, New Jersey", "848": "New Brunswick, New Jersey",
    "856": "Camden, New Jersey", "862": "Newark, New Jersey", "908": "Elizabeth, New Jersey", "973": "Newark, New Jersey",
    
    # New Mexico
    "505": "Albuquerque, New Mexico", "575": "Las Cruces, New Mexico",
    
    # New York
    "212": "New York City, New York", "315": "Syracuse, New York", "329": "New York City, New York",
    "332": "New York City, New York", "347": "New York City, New York", "363": "Hempstead, New York",
    "516": "Hempstead, New York", "518": "Albany, New York", "585": "Rochester, New York",
    "607": "Binghamton, New York", "624": "Buffalo, New York", "631": "Islip, New York",
    "646": "New York City, New York", "680": "Syracuse, New York", "716": "Buffalo, New York",
    "718": "New York City, New York", "838": "Albany, New York", "845": "Poughkeepsie, New York",
    "914": "Yonkers, New York", "917": "New York City, New York", "929": "New York City, New York", "934": "Islip, New York",
    
    # North Carolina
    "252": "Greenville, North Carolina", "336": "Greensboro, North Carolina", "472": "Greensboro, North Carolina",
    "704": "Charlotte, North Carolina", "743": "Greensboro, North Carolina", "828": "Asheville, North Carolina",
    "910": "Fayetteville, North Carolina", "919": "Raleigh, North Carolina", "980": "Charlotte, North Carolina", "984": "Raleigh, North Carolina",
    
    # North Dakota
    "701": "Fargo, North Dakota",
    
    # Ohio
    "216": "Cleveland, Ohio", "220": "Newark, Ohio", "234": "Akron, Ohio", "283": "Cincinnati, Ohio",
    "326": "Dayton, Ohio", "330": "Akron, Ohio", "380": "Columbus, Ohio", "419": "Toledo, Ohio",
    "436": "Elyria, Ohio", "440": "Parma, Ohio", "513": "Cincinnati, Ohio", "567": "Toledo, Ohio",
    "614": "Columbus, Ohio", "740": "Newark, Ohio", "937": "Dayton, Ohio",
    
    # Oklahoma
    "405": "Oklahoma City, Oklahoma", "539": "Tulsa, Oklahoma", "572": "Oklahoma City, Oklahoma",
    "580": "Lawton, Oklahoma", "918": "Tulsa, Oklahoma",
    
    # Oregon
    "458": "Eugene, Oregon", "503": "Portland, Oregon", "541": "Eugene, Oregon", "971": "Portland, Oregon",
    
    # Pennsylvania
    "215": "Philadelphia, Pennsylvania", "223": "Lancaster, Pennsylvania", "267": "Philadelphia, Pennsylvania",
    "272": "Scranton, Pennsylvania", "412": "Pittsburgh, Pennsylvania", "445": "Philadelphia, Pennsylvania",
    "484": "Allentown, Pennsylvania", "570": "Scranton, Pennsylvania", "582": "State College, Pennsylvania",
    "610": "Allentown, Pennsylvania", "717": "Lancaster, Pennsylvania", "724": "New Castle, Pennsylvania",
    "814": "Erie, Pennsylvania", "835": "Allentown, Pennsylvania", "878": "Pittsburgh, Pennsylvania",
    
    # Rhode Island
    "401": "Providence, Rhode Island",
    
    # South Carolina
    "803": "Columbia, South Carolina", "839": "Columbia, South Carolina", "843": "Charleston, South Carolina",
    "854": "Charleston, South Carolina", "864": "Greenville, South Carolina",
    
    # South Dakota
    "605": "Sioux Falls, South Dakota",
    
    # Tennessee
    "423": "Chattanooga, Tennessee", "615": "Nashville, Tennessee", "629": "Nashville, Tennessee",
    "731": "Jackson, Tennessee", "865": "Knoxville, Tennessee", "901": "Memphis, Tennessee", "931": "Clarksville, Tennessee",
    
    # Texas
    "210": "San Antonio, Texas", "214": "Dallas, Texas", "254": "Waco, Texas", "281": "Houston, Texas",
    "325": "Abilene, Texas", "346": "Houston, Texas", "361": "Corpus Christi, Texas", "409": "Beaumont, Texas",
    "430": "Tyler, Texas", "432": "Midland, Texas", "469": "Dallas, Texas", "512": "Austin, Texas",
    "682": "Fort Worth, Texas", "713": "Houston, Texas", "726": "San Antonio, Texas", "737": "Austin, Texas",
    "806": "Lubbock, Texas", "817": "Fort Worth, Texas", "830": "New Braunfels, Texas", "832": "Houston, Texas",
    "903": "Tyler, Texas", "915": "El Paso, Texas", "936": "Conroe, Texas", "940": "Denton, Texas",
    "945": "Dallas, Texas", "956": "Laredo, Texas", "972": "Dallas, Texas", "979": "College Station, Texas",
    
    # Utah
    "385": "Salt Lake City, Utah", "435": "St. George, Utah", "801": "Salt Lake City, Utah",
    
    # Vermont
    "802": "Burlington, Vermont",
    
    # Virginia
    "276": "Bristol, Virginia", "434": "Charlottesville, Virginia", "540": "Roanoke, Virginia",
    "571": "Arlington, Virginia", "686": "Richmond, Virginia", "703": "Arlington, Virginia",
    "757": "Virginia Beach, Virginia", "804": "Richmond, Virginia", "826": "Roanoke, Virginia", "948": "Virginia Beach, Virginia",
    
    # Washington
    "206": "Seattle, Washington", "253": "Tacoma, Washington", "360": "Olympia, Washington",
    "425": "Bellevue, Washington", "509": "Spokane, Washington", "564": "Olympia, Washington",
    
    # Washington, DC
    "202": "Washington, District of Columbia", "771": "Washington, District of Columbia",
    
    # West Virginia
    "304": "Charleston, West Virginia", "681": "Charleston, West Virginia",
    
    # Wisconsin
    "262": "Kenosha, Wisconsin", "274": "Green Bay, Wisconsin", "353": "Madison, Wisconsin",
    "414": "Milwaukee, Wisconsin", "534": "Eau Claire, Wisconsin", "608": "Madison, Wisconsin",
    "715": "Eau Claire, Wisconsin", "920": "Green Bay, Wisconsin",
    
    # Wyoming
    "307": "Cheyenne, Wyoming",
    
    # Territories
    "684": "Pago Pago, American Samoa",
    "671": "Hagåtña, Guam",
    "670": "Saipan, Northern Mariana Islands",
    "787": "San Juan, Puerto Rico", "939": "San Juan, Puerto Rico",
    "340": "Charlotte Amalie, U.S. Virgin Islands"
}


geolocator = Nominatim(user_agent="area_code_mapper")
final_db = {}

print("Починаємо генерацію точної бази. Це може зайняти трохи часу...")

for code, location_name in detailed_codes.items():
    try:
        # Робимо запит до API для пошуку координат
        location = geolocator.geocode(location_name)
        
        if location:
            # Розділяємо рядок на Місто та Штат
            city, state = [x.strip() for x in location_name.split(',')]
            
            final_db[code] = {
                "state": state,
                "city": city,
                "lat": location.latitude,
                "lon": location.longitude
            }
            print(f"✅ {code}: {city} ({location.latitude:.4f}, {location.longitude:.4f})")
        else:
            print(f"❌ Не вдалося знайти координати для: {location_name}")
        
        # ОБОВ'ЯЗКОВО: Затримка в 1 секунду. 
        # OpenStreetMap безкоштовний, але блокує тих, хто робить запити занадто швидко.
        time.sleep(1)
        
    except Exception as e:
        print(f"Помилка з кодом {code}: {e}")

# Зберігаємо готову базу
with open('area_codes.json', 'w', encoding='utf-8') as f:
    json.dump(final_db, f, indent=4, ensure_ascii=False)

print(f"\nГотово! Базу на {len(final_db)} кодів успішно згенеровано.")