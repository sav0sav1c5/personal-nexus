# Entry point of app

from utils.pipeline import pipeline

def main():
    print('Personal nexus running...')

    query = "Objasni mi funkcije u Python-u?"
    pipeline(query=query)

if __name__ == '__main__':

    main()