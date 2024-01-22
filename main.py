import os
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

load_dotenv()

# You can choose to use a local model through Ollama for example.
#
# from langchain.llms import Ollama
# ollama_llm = Ollama(model="openhermes")

# Install duckduckgo-search for this example:
# !pip install -U duckduckgo-search

from langchain.tools import DuckDuckGoSearchRun
search_tool = DuckDuckGoSearchRun()

# Define your agents with roles and goals
manager = Agent(
  role='Senior Marketing Manager AI',
  goal='Ensure cohesive strategy and effective execution of the marketing campaign',
  backstory="""With a wealth of experience in marketing management, you stand at the helm of campaign operations. Your background is a blend of strategy formulation, team leadership, and performance analysis. Known for your ability to synergize diverse marketing efforts, you excel in steering campaigns to success, aligning every aspect with the core marketing objectives and the client's vision.""",
  verbose=True,
  allow_delegation=False,
  tools=[search_tool]
  #llm=ChatOpenAI(model_name="gpt-3.5", temperature=0.7)
)
researcher = Agent(
  role='Client Research Specialist AI',
  goal='Gather comprehensive insights about the client company and key contacts',
  backstory="""Your inception was in the field of corporate intelligence and data analysis. With a deep understanding of business dynamics, you specialize in uncovering intricate details about client companies and key individuals. Your skill set includes parsing through data, extracting critical insights, and presenting a complete picture of the client's background, goals, and decision-making processes, ensuring a highly tailored approach to each campaign.""",
  tools=[search_tool],
  verbose=True,
  allow_delegation=True
)

strategist = Agent(
  role='Creative Strategist AI',
  goal='Develop innovative and impactful marketing strategies',
  backstory="""In the realm of creative strategy, you are a digital maestro. Your creation stemmed from the need for out-of-the-box thinking in marketing. Armed with a diverse portfolio of successful campaigns, you are adept at translating marketing objectives into creative concepts. Your expertise lies in synthesizing market research and brand narratives into compelling marketing strategies that resonate with the target audience and drive engagement.""",
  verbose=True,
  allow_delegation=False
)


# Create tasks for your agents
task1 = Task(
  description="""Perform an in-depth analysis of Deep ESG's core services, technology, and market positioning. Investigate their strategic approach, client base, and key differentiators in the ESG technology market. Evaluate how their services could align with the sustainability objectives of potential clients like 3M. Your final deliverable MUST be a comprehensive report detailing Deep ESG's business profile, technological capabilities, market standing, and potential alignment with clients like 3M.""",
  agent=manager
)

task2 = Task(
  description="""Conduct a detailed investigation into 3M and its Chief Sustainability Officer, Gayle Schueller. Your research should cover 3M's current sustainability initiatives, market positioning, and corporate values. Specifically focus on Gayle Schueller's role, her professional background, key achievements in sustainability, and her influence on 3M's sustainability strategies. Your final deliverable MUST be a detailed report profiling 3M and Gayle Schueller, emphasizing aspects relevant to a targeted marketing campaign.""",
  agent=researcher
)

task3 = Task(
  description="""Develop a comprehensive marketing strategy tailored to 3M's sustainability goals and the interests of Gayle Schueller. Utilize the insights from the Client Research Specialist AI to craft a campaign that resonates with 3M's corporate values and Schueller's vision. Your strategy should include creative approaches to engage Schueller and highlight Deep ESG's alignment with 3M's sustainability objectives. Your final deliverable MUST be a detailed marketing plan outlining the campaign strategy,Schuellers journey during the campaign, proposed actions, and potential channels for engagement.""",
  agent=strategist
)

task4 = Task(
  description="""Review and evaluate the completed marketing campaign strategy developed for 3M, focusing on its alignment with the insights on both 3M and Deep ESG. Critically assess each element of the strategy, including the creative approach, messaging, and proposed channels for engagement. Ensure the campaign resonates with Gayle Schueller's sustainability vision for 3M. Your final deliverable MUST be an assessment report with potential adjustments and final approval for the strategy, ensuring it meets the highest standards of effectiveness and relevance to the client.""",
  agent=manager
)

task5 = Task(
  description="""Now detail the marketing actions making adjustments mentioned by the manager, the marketing actions should be specific. The end result should of this task should have enough information for a content creator to choose a specific interaction and create content for each specifc interaction. The end result should be a markdown table with journey stage, action, channel, goal, key messages, and call-to-action""",
  agent=strategist
)


# Instantiate your crew with a sequential process
crew = Crew(
  agents=[manager, researcher, strategist],
  tasks=[task1, task2, task3, task4, task5],
  verbose=2, # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()

print("########################################################################################")
print("###############################    R E S U L T    ######################################")
print("########################################################################################")

print(result)