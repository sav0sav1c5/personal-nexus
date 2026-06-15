# Entry point of app

from pipeline import pipeline

def main():
    print('Personal nexus running...')
    print('Information:')
    print(' - To exit enter X')
    print(' - Verbose mode: type "v: " before your question (e.g., "v: What is Python?")')
    print(' - Time measurement is always ON for queries')
    print()

    conversation_history = []

    while True:
        user_input = input('Enter Query: ').strip()
        
        if user_input.upper() == 'X':
            print('Goodbye!')
            break
        
        if user_input == '':
            print('Please enter a question.\n')
            continue

        if user_input.lower() == 'reset':
            conversation_history = []
            print('Conversation history cleared!')
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
        system_response = pipeline(
            query=query, 
            verbose=verbose, 
            measure_time=True,
            conversation_history=conversation_history
        )

        # Save history of one iteration - query + response
        if system_response:
            conversation_history.append({'role': 'user', 'content': 'query'})
            conversation_history.append({'role': 'assistant', 'content': system_response})

if __name__ == '__main__':

    main()