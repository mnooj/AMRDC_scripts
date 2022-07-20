import ckanapi, os, sys

SERVER_URL = 'https://amrdcdata.ssec.wisc.edu/'
API_KEY = ''

DIRECTORY = sys.argv[1]
TARGET_DATASET = sys.argv[2]

def batch_upload(directory, target_dataset):
    repository = ckanapi.RemoteCKAN(SERVER_URL, apikey=API_KEY)
    for file in sorted(os.listdir(directory)):
        if not file.startswith('.'):
            repository.action.resource_create(package_id=target_dataset, name=file, upload=open(directory + '/' + file, 'rb'))
            count = count + 1
    print(target_dataset + " Files uploaded: " + str(count))

if __name__ == '__main__':
    batch_upload(DIRECTORY, TARGET_DATASET)