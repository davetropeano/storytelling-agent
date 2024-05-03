import sys, getopt, logging
from dotenv import dotenv_values
from datetime import datetime
from storytelling_agent.storytelling_agent import StoryAgent

logger = logging.getLogger(__name__)

def main(argv):
    logging.basicConfig(filename='storygen.log', level=logging.INFO)
    
    config = dotenv_values(".env")
    model = 'anthropic/claude-3-haiku'
    writer = StoryAgent(config['OPENROUTER_BASE_URL'], config['OPENROUTER_API_KEY'], form='novel', backend='openrouter', model=model)
    topic = 'cozy mystery at a New Hampshire bookstore'
    plot_template = 'save the cat'
    book_folder = datetime.now().strftime('%Y%m%d')

    try:
        opts, args = getopt.getopt(argv,"ht:m:p:b:",["topic=","model=","plot="])
    except getopt.GetoptError:
        print ('storygen.py -t <topic> -m <model> -p <plot template>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('storygen.py -t <topic> -m <model> -p <plot template>')
            print(f"topic default is: {topic}")
            print(f"model default is: {model}")
            print(f"plot template default is: {plot_template}")
            print(f"book location default is {book_folder}")
            sys.exit()
        elif opt in ("-t", "--topic"):
            topic = arg
        elif opt in ("-m", "--model"):
            model = arg
        elif opt in ("-p", "--plot"):
            plot_template = arg
        elif opt in ("-b", "--book"):
            book_folder = arg


    logger.info(f'Topic: {topic}, Plot Template: {plot_template}, Model: {model}')    
    writer.generate_story(topic, plot_template, book_folder)

if __name__ == "__main__":
   main(sys.argv[1:])

