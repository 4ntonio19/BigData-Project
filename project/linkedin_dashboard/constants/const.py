from project.linkedin_dashboard.Enums.dataset_enum import DatasetName


ALL_STATES = [
    "AL",  # Alabama
    "AK",  # Alaska
    "AZ",  # Arizona
    "AR",  # Arkansas
    "CA",  # California
    "CO",  # Colorado
    "CT",  # Connecticut
    "DE",  # Delaware
    "DC",  # District of Columbia
    "FL",  # Florida
    "GA",  # Georgia
    "HI",  # Hawaii
    "ID",  # Idaho
    "IL",  # Illinois
    "IN",  # Indiana
    "IA",  # Iowa
    "KS",  # Kansas
    "KY",  # Kentucky
    "LA",  # Louisiana
    "ME",  # Maine
    "MD",  # Maryland
    "MA",  # Massachusetts
    "MI",  # Michigan
    "MN",  # Minnesota
    "MS",  # Mississippi
    "MO",  # Missouri
    "MT",  # Montana
    "NE",  # Nebraska
    "NV",  # Nevada
    "NH",  # New Hampshire
    "NJ",  # New Jersey
    "NM",  # New Mexico
    "NY",  # New York
    "NC",  # North Carolina
    "ND",  # North Dakota
    "OH",  # Ohio
    "OK",  # Oklahoma
    "OR",  # Oregon
    "PA",  # Pennsylvania
    "RI",  # Rhode Island
    "SC",  # South Carolina
    "SD",  # South Dakota
    "TN",  # Tennessee
    "TX",  # Texas
    "UT",  # Utah
    "VT",  # Vermont
    "VA",  # Virginia
    "WA",  # Washington
    "WV",  # West Virginia
    "WI",  # Wisconsin
    "WY",  # Wyoming
    "PR",  # Puerto Rico
    "US",  # United States
    "ON",  # Ontario
    "QC",  # Quebec
    "PH",  # Philippines
    "ZA",  # South Africa
    "GM",  # The Gambia
    "NL",  # Netherlands
    "BR",  # Brazil
]

EXTERNAL_DICT = {
    "NJ": "NJ",
    "CO": "CO",
    "OH": "OH",
    "NY": "NY",
    "IA": "IA",
    "NC": "NC",
    "CA": "CA",
    "NE": "NE",
    "FL": "FL",
    "MI": "MI",
    "MO": "MO",
    "TN": "TN",
    "AK": "AK",
    "RI": "RI",
    "Greater Philadelphia": "PA",
    "AL": "AL",
    "GA": "GA",
    "Los Angeles Metropolitan Area": "CA",
    "TX": "TX",
    "PA": "PA",
    "MA": "MA",
    "AZ": "AZ",
    "VA": "VA",
    "WA": "WA",
    "WI": "WI",
    "HI": "HI",
    "Dallas-Fort Worth Metroplex": "TX",
    "New York City Metropolitan Area": "NY",
    "LA": "LA",
    "UT": "UT",
    "IN": "IN",
    "MN": "MN",
    "MD": "MD",
    "KY": "KY",
    "Greensboro--Winston-Salem--High Point Area": "NC",
    "Raleigh-Durham-Chapel Hill Area": "NC",
    "OR": "OR",
    "NM": "NM",
    "IL": "IL",
    "Nebraska Metropolitan Area": "NE",
    "MT": "MT",
    "Greater Minneapolis-St. Paul Area": "MN",
    "Ohio Metropolitan Area": "OH",
    "OK": "OK",
    "DC": "DC",
    "San Francisco Bay Area": "CA",
    "Cincinnati Metropolitan Area": "OH",
    "Greater Phoenix Area": "AZ",
    "MS": "MS",
    "Washington DC-Baltimore Area": "DC",
    "South Carolina Metropolitan Area": "SC",
    "SC": "SC",
    "Louisville Metropolitan Area": "KY",
    "KS": "KS",
    "Denver Metropolitan Area": "CO",
    "Huntsville-Decatur-Albertville Area": "AL",
    "AR": "AR",
    "Texas Metropolitan Area": "TX",
    "CT": "CT",
    "San Diego Metropolitan Area": "CA",
    "Greater Tampa Bay Area": "FL",
    "NV": "NV",
    "Oregon Metropolitan Area": "OR",
    "Greater Asheville": "NC",
    "Greater Pittsburgh Region": "PA",
    "Illinois Metropolitan Area": "IL",
    "ID": "ID",
    "Little Rock Metropolitan Area": "AR",
    "South Carolina Area": "SC",
    "Greater New Orleans Region": "LA",
    "NH": "NH",
    "WY": "WY",
    "Greater Sacramento": "CA",
    "Las Vegas Metropolitan Area": "NV",
    "Greater Rockford Area": "IL",
    "Greater Grand Junction Area": "CO",
    "Greater Flagstaff Area": "AZ",
    "Atlanta Metropolitan Area": "GA",
    "Detroit Metropolitan Area": "MI",
    "Greater St. Louis": "MO",
    "SD": "SD",
    "ND": "ND",
    "DE": "DE",
    "Alabama Area": "AL",
    "Nashville Metropolitan Area": "TN",
    "Greater Indianapolis": "IN",
    "WV": "WV",
    "VT": "VT",
    "Greater Houston": "TX",
    "Greater Cleveland": "OH",
    "Erie-Meadville Area": "PA",
    "Appleton-Oshkosh-Neenah Area": "WI",
    "Kansas Metropolitan Area": "KS",
    "Greater Chicago Area": "IL",
    "Buffalo-Niagara Falls Area": "NY",
    "Massachusetts Metropolitan Area": "MA",
    "Killeen-Temple Area": "TX",
    "ME": "ME",
    "Wisconsin Metropolitan Area": "WI",
    "Salt Lake City Metropolitan Area": "UT",
    "ON": "ON",
    "Greater Boston": "MA",
    "Greater Hartford": "CT",
    "Greater Jefferson City Area": "MO",
    "Kansas City Metropolitan Area": "MO",
    "Greater Seattle Area": "WA",
    "Miami-Fort Lauderdale Area": "FL",
    "New York Metropolitan Area": "NY",
    "Greater Bloomington Area": "IN",
    "Shreveport-Bossier City Area": "LA",
    "Dayton Metropolitan Area": "OH",
    "Beaumont-Port Arthur Area": "TX",
    "North Port-Sarasota Area": "FL",
    "Crestview-Fort Walton Beach-Destin Area": "FL",
    "Urbana-Champaign Area": "IL",
    "Omaha Metropolitan Area": "NE",
    "Greater Palm Bay-Melbourne-Titusville Area": "FL",
    "Greater Eugene-Springfield Area": "OR",
    "North Carolina Metropolitan Area": "NC",
    "Greater Chattanooga": "TN",
    "Greater Corpus Christi Area": "TX",
    "Greater Augusta Area": "GA",
    "Greater Salisbury Area": "MD",
    "Greater Lansing": "MI",
    "NAMER": "US",
    "Greater Macon": "GA",
    "Greater Missoula Area": "MT",
    "Oklahoma City Metropolitan Area": "OK",
    "Cape Coral Metropolitan Area": "FL",
    "College Station-Bryan Area": "TX",
    "MI Area": "MI",
    "Greater Orlando": "FL",
    "Greater Panama City Area": "FL",
    "Maui": "HI",
    "Charlotte Metro": "NC",
    "Greater Kennewick Area": "WA",
    "San Angelo Area": "TX",
    "Knoxville Metropolitan Area": "TN",
    "Utica-Rome Area": "NY",
    "Greater Kalamazoo Area": "MI",
    "Louisiana Metropolitan Area": "LA",
    "Greater Morgantown Area": "WV",
    "New Bern-Morehead City Area": "NC",
    "Spokane-Coeur d'Alene Area": "ID",
    "Philippines": "PH",
    "Greater Milwaukee": "WI",
    "Greater Syracuse-Auburn Area": "NY",
    "State College-DuBois Area": "PA",
    "Greater Savannah Area": "GA",
    "Baton Rouge Metropolitan Area": "LA",
    "Twin Falls Area": "ID",
    "Peoria Metropolitan Area": "IL",
    "Des Moines Metropolitan Area": "IA",
    "Wausau-Stevens Point Area": "WI",
    "Honolulu Metropolitan Area": "HI",
    "Greater Anchorage Area": "AK",
    "Greater Scranton Area": "PA",
    "Gainesville Metropolitan Area": "FL",
    "Boise Metropolitan Area": "ID",
    "Greater Myrtle Beach Area": "SC",
    "Greater Tuscaloosa Area": "AL",
    "Northeastern United States": "US",
    "Greater Idaho Falls": "ID",
    "Waco Area": "TX",
    "Metropolitan Fresno": "CA",
    "Greater Richmond Region": "VA",
    "Greater Reno Area": "NV",
    "Metro Jacksonville": "FL",
    "Greater Jackson Area": "MS",
    "Lancaster Metropolitan Area": "PA",
    "Valdosta Area": "GA",
    "Georgia Area": "GA",
    "Netherlands": "NL",
    "United States": "US",
    "Greater Dothan": "AL",
    "Indiana Metropolitan Area": "IN",
    "Greater San Luis Obispo Area": "CA",
    "Modesto-Merced Area": "CA",
    "Greater Amarillo Area": "TX",
    "La Crosse-Onalaska Area": "WI",
    "Missouri Area": "MO",
    "Grand Rapids Metropolitan Area": "MI",
    "Lubbock-Levelland Area": "TX",
    "Quad Cities Metropolitan Area": "IL",
    "Memphis Metropolitan Area": "TN",
    "Blacksburg-Christiansburg-Radford Area": "VA",
    "Greater Tucson Area": "AZ",
    "Tulsa Metropolitan Area": "OK",
    "Iowa City-Cedar Rapids Area": "IA",
    "Redding-Red Bluff Area": "CA",
    "Greater Wilmington Area": "NC",
    "Greater Pittsfield Area": "MA",
    "Greater Harrisburg Area": "PA",
    "Virginia Metropolitan Area": "VA",
    "Waterloo-Cedar Falls Area": "IA",
    "Greater Lynchburg Area": "VA",
    "Topeka Metropolitan Area": "KS",
    "Mobile Metropolitan Area": "AL",
    "Eau Claire-Menomonie Area": "WI",
    "Greater Billings Area": "MT",
    "Greater Bismarck Area": "ND",
    "Greater Mansfield Area": "OH",
    "Greater Madison Area": "WI",
    "Greater Bend Area": "OR",
    "El Paso Metropolitan Area": "TX",
    "Tallahassee Metropolitan Area": "FL",
    "South Bend-Mishawaka Region": "IN",
    "Greater Fort Wayne": "IN",
    "Illinois Area": "IL",
    "Youngstown-Warren area": "OH",
    "Sheboygan Metropolitan Area": "WI",
    "North Carolina Area": "NC",
    "Pensacola Metropolitan Area": "FL",
    "Albuquerque-Santa Fe Metropolitan Area": "NM",
    "Greater Sioux Falls Area": "SD",
    "IL Area": "IL",
    "Pueblo-Cañon City Area": "CO",
    "Greater Chico Area": "CA",
    "Greater Biloxi Area": "MS",
    "Houma-Thibodaux Area": "LA",
    "Brownsville Metropolitan Area": "TX",
    "Johnson City-Kingsport-Bristol Area": "TN",
    "Maine Metropolitan Area": "ME",
    "QC": "QC",
    "Bowling Green Metropolitan Area": "KY",
    "Greater Roanoke Area": "VA",
    "Canada": "CA",
    "Greater Goldsboro Area": "NC",
    "Greater Charlottesville Area": "VA",
    "Greater Fort Collins Area": "CO",
    "Rocky Mount-Wilson Area": "NC",
    "Midland-Odessa Area": "TX",
    "Greater Yakima Area": "WA",
    "Minnesota Area": "MN",
    "Bellingham Metropolitan Area": "WA",
    "NC Area": "NC",
    "AR Area": "AR",
    "Greater Columbus Area": "OH",
    "Greater Colorado Springs Area": "CO",
    "Lawton Area": "OK",
    "AZ Area": "AZ",
    "Greater McAllen Area": "TX",
    "Greater Lexington Area": "KY",
    "Greater Enid Area": "OK",
    "Greater Bangor Area": "ME",
    "Greater Montgomery Area": "AL",
    "Visalia-Hanford Area": "CA",
    "Greater Salinas Area": "CA",
    "The Gambia": "GM",
    "Lake Charles-Jennings Area": "LA",
    "Greater Ocala Area": "FL",
    "Greater Bakersfield Area": "CA",
    "Medford-Grants Pass Area": "OR",
    "Greater Terre Haute Area": "IN",
}

GLOBAL_DATASETS = {}

SKILLS_LIST = ["DSGN", "PRDM", "QA", "IT"]
SKILLS_WITH_DATASET_MAPPING = {
        "DSGN": DatasetName.PREDICT_JOB_POSTINGS_DSGN,
        "PRDM": DatasetName.PREDICT_JOB_POSTINGS_PRDM,
        "QA": DatasetName.PREDICT_JOB_POSTINGS_QA,
        "IT": DatasetName.PREDICT_JOB_POSTINGS_IT
    }
CACHED_PROCESSED_DF = None
