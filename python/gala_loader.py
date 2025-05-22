import json, pandas as pd
import pywikibot
from pywikibot import pagegenerators
import time

def read_citations_from_csv(csv_file):
    """Read citation data from a CSV file."""
    df = pd.read_csv(csv_file,
                     usecols=['url', 'published_at', 'latitude', 'longitude', 'locale',
                              'authors', 'dek', 'kicker', 'title'])
    return df

def create_or_find_item(site, title, url):
    """Create a new item or find an existing one based on title and url."""
    # First, try to find if the item already exists
    #query = f'haswbstatement:P31=Q155207 AND "{title}"'
    query = f'"{title}" haswbstatement:P31=Q155207'
    generator = pagegenerators.SearchPageGenerator(query, site=site)
    
    # Check the first few results
    for page in generator:
        #print(page)
        item = pywikibot.ItemPage(site, page.title())
        item_dict = item.get()
        
        # Check if this is indeed our item by comparing title and author
        if 'en' in item_dict['labels']:
            if title.lower() in item_dict['labels']['en'].lower():
                return item, False  # Item found, not new
    
    # If we didn't find a matching item, create a new one
    new_item = pywikibot.ItemPage(site)
    new_item.editLabels(labels={'en': title})
    
    return new_item, True  # New item created

def add_statement(item, property_id, value):
    """Add statement with automatic type detection based on property."""
    # Get property information
    prop = pywikibot.PropertyPage(item.site, property_id)
    prop_dict = prop.get()
    expected_type = prop_dict.get('datatype')
    
    print(f"Property {property_id} expects type: {expected_type}")
    
    claim = pywikibot.Claim(item.site, property_id)
    
    # Set target based on expected data type
    if expected_type == 'wikibase-item':
        # Expects ItemPage
        if isinstance(value, str):
            value = pywikibot.ItemPage(item.site, value)
        claim.setTarget(value)
    elif expected_type == 'string':
        # Expects string
        if isinstance(value, pywikibot.ItemPage):
            value = value.id
        claim.setTarget(str(value))
    elif expected_type == 'url':
        # Expects URL string
        if isinstance(value, pywikibot.ItemPage):
            # Convert ItemPage to a URL pointing to that item
            value = f"https://wikidata.org/wiki/{value.id}"
        elif isinstance(value, str) and value.startswith('Q'):
            # Convert Q-ID to URL
            value = f"https://wikidata.org/wiki/{value}"
        claim.setTarget(value)
    elif expected_type == 'time':
        claim.setTarget(value)
    elif expected_type == 'monolingualtext':
        claim.setTarget(value)
    else:
        print(f"Unknown data type: {expected_type}")
        return False
    
    try:
        item.addClaim(claim)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def process_citations(csv_file):
    """Process all citations from the CSV file."""
    #site = pywikibot.Site('wikidata', 'wikidata')
    site = pywikibot.Site('test', 'wikidata')
    site.login()

    citations = read_citations_from_csv(csv_file)
    for index, row in citations.iterrows():
        # Extract basic info
        title = str(row['title']).strip()
        url = row['url']

        # Can't handle non-English locale for now
        if row['locale'] != 'en':
            continue
        
        if not title or len(title) < 5:
            print(f"Skipping entry with missing title: {row}")
            continue
            
        print(f"Processing: {title} at {url}")

        # Create or find the item
        try:
            item, is_new = create_or_find_item(site, title, url)

            print(item)

            if is_new:
                print(f"Created new item for: {title}")

                # Add instance of case study (P31:Q155207)
                add_statement(item, 'P31', 'Q155207')
                
                # Add instance of publication (P31:Q732557)
                add_statement(item, 'P31', 'Q732557')
                
                # Add instance of title (P1476)
                # add_statement(item, 'P1476', title)
                
                # Add instance of full work available at URL (P953)
                add_statement(item, 'P953', url)

                authors = json.loads(row['authors'])
                for a in authors:
                    name = a['name'].strip()
                    #if name:
                        # Add instance of author name string (P2093)
                        # add_statement(item, 'P2093', name)

                # Add instance of published in Gala (P1433:Q130549584)
                add_statement(item, 'P1433', 'Q130549584')

                # Add instance of copyright license CC BY 4.0 (P275:Q20007257)
                # add_statement(item, 'P275', 'Q20007257')

                # Add instance of copyright status copyrighted (P6216:Q50423863)
                add_statement(item, 'P6216', 'Q50423863')
                
                # Sleep to avoid overwhelming the API
                time.sleep(1)
            else:
                print(f"Found existing item for: {title}")
            
        except Exception as e:
            print(f"Error processing {title}: {str(e)}")


if __name__ == "__main__":
    csv_file = "gala.csv"  # Replace with your CSV file path
    process_citations(csv_file)
