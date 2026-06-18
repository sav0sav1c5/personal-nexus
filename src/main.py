# Entry point of app

from pipeline import pipeline
from utils import parse_user_input, format_help, get_index_status
from evaluation.evaluate import run_evaluation

def main():
    print(format_help())

    # Show index status
    index_status = get_index_status()

    if index_status['needs_indexing']:
        print('No index found. Indexes will be created on first query!')
    else:
        print(f'Index found at: {index_status['path']}')

    conversation_history = []

    while True:
        user_input = input('Enter Query: ').strip()
        
        # Parse user input
        action, verbose, query = parse_user_input(user_input)

        if action == 'exit':
            print('Goodbye!')
            break
        
        if action == 'reset':
            conversation_history = []
            print('Conversation history cleared!')
            continue

        if action == 'empty':
            print('Please enter a question.\n')
            continue

        if action == 'eval':
            print('\nRunning RAGAS evaluation')
            run_evaluation(verbose=True)
        
        # If action is 'query' add new row for better reading
        print()
        
        # Run pipeline with time measurement
        system_response = pipeline(
            query=query, 
            verbose=verbose, 
            measure_time=True,
            conversation_history=conversation_history
        )

        # Save history of one iteration - query + response
        if system_response:
            conversation_history.append({'role': 'user', 'content': query})
            conversation_history.append({'role': 'assistant', 'content': system_response})

if __name__ == '__main__':

    main()