import ckanapi, os, sys

SERVER_URL = 'https://amrdcdata.ssec.wisc.edu/'
API_KEY = ''

## To run this script from the command line:    python batch_upload.py "{AWS NAME}" "{YEAR}" "{DATA_DIRECTORY}"
## For example:  $ python batch_upload.py "Byrd" "2001" "/Users/mnoojin/Desktop/2001/Byrd/"
NAME = sys.argv[1]
YEAR = sys.argv[2]
DIRECTORY = sys.argv[3]

def batch_upload(directory, target_dataset):
    repository = ckanapi.RemoteCKAN(SERVER_URL, apikey=API_KEY)
    for file in sorted(os.listdir(directory)):
        if not file.startswith('.'):
            repository.action.resource_create(package_id=target_dataset, name=file, upload=open(directory + '/' + file, 'rb'))
            count = count + 1
    print(target_dataset + " Files uploaded: " + str(count))

def create_dataset(name, year):

    dataset_dict = {
        "title": f"{name} Automatic Weather Station, {year} Reader format three-hour observational data."
        "isopen": True,
        "license_id": "cc-by",
        "license_title": "Creative Commons Attribution",
        "license_url": "http://www.opendefinition.org/licenses/cc-by",
        "maintainer": "Antarctic Meteorological Research and Data Center",
        "maintainer_email": "amrdc@amrdc.ssec.wisc.edu",
        "name": dataset_dict["title"].lower().replace(",","").replace(".","").replace(" ", "-")
        "organization": {
            "approval_status": "approved",
            "created": "2021-06-09T15:09:00.395998",
            "description": "Antarctic Meteorological Research and Data Center",
            "id": "0af17158-f668-4a7c-a0a0-3ff481fe4f37",
            "image_url": "2021-06-09-150900.386477amrdc-gradient-regular-circle1.png",
            "is_organization": True,
            "name": "amrdc",
            "revision_id": "70c04035-8be2-459f-81c4-2267776ae950",
            "state": "active",
            "title": "AMRDC",
            "type": "organization"
        },
        "owner_org": "0af17158-f668-4a7c-a0a0-3ff481fe4f37",
        "private": False,
        "state": "active",
        "type": "dataset",
    }

    repository = ckanapi.RemoteCKAN(SERVER_URL, apikey=API_KEY)
    repository.call_action('package_create', dataset_dict)
    print(f"Dataset created : {name}")
    return dataset_dict["name"]
    
if __name__ == '__main__':
    target_dataset = create_dataset(NAME, YEAR)
    batch_upload(DIRECTORY, target_dataset)
