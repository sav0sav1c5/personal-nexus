# RAGAS evaluation of PAG system

from ragas import evaluate, EvaluationDataset
from ragas.dataset_schema import SingleTurnSample
from retrieval.retriever import retrieve
from generation.generator import generate
from evaluation.eval_config import METRICS, TEST_QUESTIONS, TEST_QUESTIONS_SUBSET, run_config

def collect_data(test_questions: list, verbose: bool = False) -> tuple:
    """ 
    It goes through each question, runs the RAG pipeline and collects 
    all necessary data for RAGAS evaluation. 

    Returns: 
    tuple: (questions, answers, contexts, ground_truths) 
    """
        
    samples = []

    for item in test_questions:
        question = item['question']
        ground_truth = item['ground_truth']

        retrieved_chunks = retrieve(query=question, n_results=3)

        context_texts = [chunk['content'] for chunk in retrieved_chunks]

        full_answer = ''
        for token in generate(query=question, retrieved_chunks=retrieved_chunks, conversation_history=[]):
            full_answer += token

        sample = SingleTurnSample(
            user_input=question,
            response=full_answer,
            retrieved_contexts=context_texts,
            reference=ground_truth
        )

        samples.append(sample)
    
    return samples

def format_data(samples: list) -> EvaluationDataset: 
    """ 
    Packs a list of SingleTurnSample objects into an EvaluationDataset. 

    Returns: 
    EvaluationDataset: RAGAS dataset object ready for evaluation 
    """ 

    # EvaluationDataset is a new format in 0.4.x that replaces HuggingFace Dataset 
    return EvaluationDataset(samples=samples)

def show_data(results):
    """Displays the evaluation results in a human-readable format."""

    print("\n========== EVALUATION RESULTS ==========")
    print(results)

    print("\n--- Detailed breakdown per question ---")
    df = results.to_pandas()
    print(df.to_string())
    print("========================================\n")

def run_evaluation(verbose: bool = False) -> None: 
    """ 
    Runs a complete RAGAS evaluation. 

    Args: 
    verbose (bool): If True, print the progress 
    """ 

    if verbose: 
        print("Collecting data from RAG pipeline...") 

    samples = collect_data(test_questions=TEST_QUESTIONS_SUBSET, verbose=verbose) 
    dataset = format_data(samples) 

    if verbose: 
        print(f"Dataset ready ({len(samples)} samples). Running RAGAS...\n") 

    results = evaluate( 
        dataset=dataset, 
        metrics=METRICS,
        run_config=run_config
    ) 

    show_data(results=results)