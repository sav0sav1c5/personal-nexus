# Entry point of app

from src.pipeline import pipeline

def main():
    print('Personal nexus running...')
    print('Information:')
    print(' - To exit enter X')
    print(' - Verbose mode: type "v: " before your question (e.g., "v: What is Python?")')
    print(' - Time measurement is always ON for queries')
    print()

    while True:
        user_input = input('Enter Query: ').strip()
        
        if user_input.upper() == 'X':
            print('Goodbye!')
            break
        
        if user_input == '':
            print('Please enter a question.\n')
            continue
        
        # Check for verbose mode (starts with "v: ")
        if user_input.lower().startswith('v: '):
            verbose = True
            query = user_input[3:].strip()  # Remove "v: " prefix
        else:
            verbose = False
            query = user_input
        
        if not query:
            print('Please enter a question.\n')
            continue
        
        # Run pipeline with time measurement
        answer = pipeline(query=query, verbose=verbose, measure_time=True)

if __name__ == '__main__':

    main()